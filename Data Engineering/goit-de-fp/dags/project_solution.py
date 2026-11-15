"""Stage 4: use SparkSubmitOperator to run the three Spark applications in order."""
import os
from pathlib import Path

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import pendulum

PROJECT_ROOT = Path(os.environ.get("OLYMPIC_PROJECT_ROOT", Path(__file__).resolve().parents[1]))
JOBS = ("landing_to_bronze", "bronze_to_silver", "silver_to_gold")

with DAG(
    dag_id="olympic_batch_data_lake",
    description="Olympic CSV to Bronze, Silver and Gold Parquet",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["spark", "parquet", "olympics"],
) as project_solution:
    options = {}
    if os.getenv("OLYMPIC_SPARK_PY_FILES"):
        options["py_files"] = os.environ["OLYMPIC_SPARK_PY_FILES"]
    landing_to_bronze, bronze_to_silver, silver_to_gold = [
        SparkSubmitOperator(
            task_id=module,
            conn_id="spark-default",
            application=str(PROJECT_ROOT / "batch" / f"{module}.py"),
            application_args=["--root", os.getenv("LAKE_ROOT", str(PROJECT_ROOT / "lake"))],
            name=f"olympics-{module}",
            verbose=False,
            **options,
        )
        for module in JOBS
    ]
    landing_to_bronze >> bronze_to_silver >> silver_to_gold
