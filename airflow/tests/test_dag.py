"""Does the DAG load, and is it wired the way we meant? (The pattern from Airflow's best-practices docs.)"""

import pytest
from airflow.dag_processing.dagbag import DagBag

from conftest import DAGS_DIR


@pytest.fixture(scope="module")
def dagbag():
    return DagBag(dag_folder=str(DAGS_DIR))


def test_no_import_errors(dagbag):
    assert dagbag.import_errors == {}


def test_dag_has_the_expected_tasks_in_order(dagbag):
    dag = dagbag.dags["shop_daily_revenue"]  # read from the parsed files; get_dag() would also query the metadata database
    expected = {
        "extract": {"transform"},
        "transform": {"check"},
        "check": {"load"},
        "load": set(),
    }
    assert set(dag.task_dict) == set(expected)
    for task_id, downstream in expected.items():
        assert dag.get_task(task_id).downstream_task_ids == downstream


def test_dag_does_not_backfill(dagbag):
    dag = dagbag.dags["shop_daily_revenue"]  # read from the parsed files; get_dag() would also query the metadata database
    assert dag.catchup is False
