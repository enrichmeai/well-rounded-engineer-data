"""Runs `dbt build` exactly as the README does, then checks the finished mart against answers worked out by hand."""

import os
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import duckdb
import pytest

PROJECT_DIR = Path(__file__).resolve().parents[1] / "shop"
DBT = Path(sys.executable).parent / "dbt"  # the dbt installed in the same virtual environment


@pytest.fixture(scope="module")
def built_db(tmp_path_factory) -> Path:
    db_path = tmp_path_factory.mktemp("dbt") / "shop.duckdb"
    env = {**os.environ, "SHOP_DUCKDB_PATH": str(db_path)}
    result = subprocess.run(
        [str(DBT), "build", "--profiles-dir", ".", "--target-path", str(db_path.parent / "target")],
        cwd=PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True,
    )
    print(result.stdout[-3000:])
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]
    return db_path


def test_dim_customers_matches_hand_worked_answers(built_db):
    with duckdb.connect(str(built_db), read_only=True) as con:
        rows = con.sql(
            "SELECT customer_name, orders_placed, first_order_date::VARCHAR, lifetime_revenue "
            "FROM dim_customers ORDER BY customer_id"
        ).fetchall()
    assert rows == [
        ("Asha", 4, "2026-01-10", Decimal("54.00")),
        ("Ben", 3, "2026-01-28", Decimal("6.00")),  # 25.00 cancelled, 109 not priced yet
        ("Chloe", 2, "2026-02-03", Decimal("49.00")),
        ("Dev", 1, "2026-02-21", Decimal("18.00")),
        ("Ema", 0, None, Decimal("0.00")),  # never ordered, still listed
    ]


def test_fct_orders_flags_revenue(built_db):
    with duckdb.connect(str(built_db), read_only=True) as con:
        not_revenue = con.sql("SELECT order_id FROM fct_orders WHERE NOT is_revenue ORDER BY order_id").fetchall()
    assert not_revenue == [(106,), (109,)]  # 106 cancelled, 109 has no amount
