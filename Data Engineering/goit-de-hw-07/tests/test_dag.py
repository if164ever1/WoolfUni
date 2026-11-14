import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("olympic_medal_counts", ROOT / "dags/olympic_medal_counts.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MedalCountsTest(unittest.TestCase):
    def test_task_graph(self):
        dag = MODULE.dag
        medal_tasks = set(MODULE.BRANCH_TASKS.values())
        self.assertEqual(len(dag.tasks), 8)
        self.assertEqual(dag.get_task("create_table").downstream_task_ids, {"choose_medal"})
        self.assertEqual(dag.get_task("choose_medal").downstream_task_ids, {"branch_by_medal"})
        self.assertEqual(dag.get_task("branch_by_medal").downstream_task_ids, medal_tasks)
        delay = dag.get_task("delay_before_sensor")
        self.assertEqual(delay.upstream_task_ids, medal_tasks)
        self.assertEqual(delay.trigger_rule, "none_failed_min_one_success")
        self.assertEqual(delay.downstream_task_ids, {"check_latest_record"})

    def test_each_medal_branches_and_binds_its_own_sql_parameters(self):
        for medal in ("Bronze", "Silver", "Gold"):
            with self.subTest(medal=medal), patch.object(MODULE.random, "choice", return_value=medal) as choice:
                self.assertEqual(MODULE.choose_medal(), medal)
                choice.assert_called_once_with(("Bronze", "Silver", "Gold"))
                ti = Mock()
                ti.xcom_pull.return_value = medal
                task_id = MODULE.choose_branch(ti)
                ti.xcom_pull.assert_called_once_with(task_ids="choose_medal")
                self.assertEqual(task_id, f"count_{medal.lower()}")
                self.assertEqual(MODULE.dag.get_task(task_id).parameters, (medal, medal))

    def test_freshness_at_microsecond_precision(self):
        for age, expected in [(-1, False), (0, True), (29_999_999, True),
                              (30_000_000, True), (30_000_001, False), (35_000_000, False)]:
            with self.subTest(age=age):
                self.assertEqual(MODULE.is_fresh(age), expected)
                self.assertEqual(MODULE.is_stale(age), not expected)
        self.assertTrue(MODULE.dag.get_task("check_latest_record").fail_on_empty)

    def test_delay_uses_trigger_parameter(self):
        with patch.object(MODULE.time, "sleep") as sleep:
            for seconds in (5, 35):
                MODULE.wait_before_sensor({"delay_seconds": seconds})
                sleep.assert_called_with(seconds)


if __name__ == "__main__":
    unittest.main()
