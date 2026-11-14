"""Count one randomly selected Olympic medal type and check the saved row."""
import logging
import random
import time
from datetime import datetime, timezone

from airflow import DAG
from airflow.models.param import Param
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.utils.trigger_rule import TriggerRule

MYSQL_CONN_ID = "olympic_mysql"
MEDALS = ("Bronze", "Silver", "Gold")
BRANCH_TASKS = {medal: f"count_{medal.lower()}" for medal in MEDALS}
MAX_AGE_US = 30_000_000
LOG = logging.getLogger(__name__)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS olympic_medal_counts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    medal_type VARCHAR(6) NOT NULL,
    `count` BIGINT UNSIGNED NOT NULL,
    created_at DATETIME(6) NOT NULL,
    INDEX idx_created_at_id (created_at, id)
)
"""

INSERT_COUNT_SQL = """
INSERT INTO olympic_medal_counts (medal_type, `count`, created_at)
SELECT %s, COUNT(*), UTC_TIMESTAMP(6)
FROM olympic_dataset.athlete_event_results
WHERE medal = %s
"""

LATEST_AGE_SQL = """
SELECT TIMESTAMPDIFF(MICROSECOND, created_at, UTC_TIMESTAMP(6)) AS age_us
FROM olympic_medal_counts
ORDER BY created_at DESC, id DESC
LIMIT 1
"""


def choose_medal():
    medal = random.choice(MEDALS)
    LOG.info("Randomly selected medal: %s", medal)
    return medal  # PythonOperator stores the return value in XCom.


def choose_branch(ti):
    medal = ti.xcom_pull(task_ids="choose_medal")
    return BRANCH_TASKS[medal]


def wait_before_sensor(params):
    seconds = params["delay_seconds"]
    LOG.info("Sleeping for %s seconds before the freshness check", seconds)
    time.sleep(seconds)


def is_stale(age_us):
    LOG.info("Latest row age: %.3f seconds (maximum: 30 seconds)", age_us / 1_000_000)
    return not 0 <= age_us <= MAX_AGE_US


def is_fresh(age_us):
    # An age of zero is valid even though the default SqlSensor check
    # treats numeric zero as false.
    return 0 <= age_us <= MAX_AGE_US


with DAG(
    dag_id="olympic_medal_counts",
    description="Count one Olympic medal type and verify MySQL record freshness",
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 0},
    params={"delay_seconds": Param(5, type="integer", minimum=0, maximum=120)},
    tags=["goit", "mysql", "olympics"],
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=MYSQL_CONN_ID,
        sql=CREATE_TABLE_SQL,
        do_xcom_push=False,
    )
    random_medal = PythonOperator(task_id="choose_medal", python_callable=choose_medal)
    branch = BranchPythonOperator(task_id="branch_by_medal", python_callable=choose_branch)
    counts = [
        SQLExecuteQueryOperator(
            task_id=BRANCH_TASKS[medal],
            conn_id=MYSQL_CONN_ID,
            sql=INSERT_COUNT_SQL,
            parameters=(medal, medal),
            do_xcom_push=False,
        )
        for medal in MEDALS
    ]
    delay = PythonOperator(
        task_id="delay_before_sensor",
        python_callable=wait_before_sensor,
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )
    check = SqlSensor(
        task_id="check_latest_record",
        conn_id=MYSQL_CONN_ID,
        sql=LATEST_AGE_SQL,
        success=is_fresh,
        failure=is_stale,
        fail_on_empty=True,
        mode="poke",
        poke_interval=1,
        timeout=10,
    )

    create_table >> random_medal >> branch >> counts >> delay >> check
