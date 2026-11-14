"""Runs the whole DAG once, the way `airflow dags test` does: real tasks, a throwaway SQLite metadata database.

This is the slow test (about 10 seconds): it creates Airflow's database, then runs every task in order.
"""

import os
import subprocess
import sys
from pathlib import Path

import duckdb

AIRFLOW = Path(sys.executable).parent / "airflow"  # the airflow installed in the same virtual environment


def test_airflow_dags_test_runs_every_task(tmp_path):
    env = {
        **os.environ,
        "AIRFLOW_HOME": str(tmp_path / "airflow-home"),
        "SHOP_ETL_DIR": str(tmp_path / "output"),
    }
    for command in (["db", "migrate"], ["dags", "test", "shop_daily_revenue", "2026-11-14"]):
        result = subprocess.run([str(AIRFLOW), *command], env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]

    with duckdb.connect(str(tmp_path / "output" / "shop.duckdb"), read_only=True) as con:
        assert con.execute("SELECT count(*) FROM daily_revenue").fetchone() == (8,)
