"""The ETL steps tested as plain Python: no scheduler, no metadata database."""

from datetime import date
from decimal import Decimal
from pathlib import Path

import duckdb
import pytest

import shop_etl

SOURCE_CSV = Path(__file__).resolve().parents[1] / "data" / "orders.csv"


def test_pipeline_end_to_end(tmp_path):
    orders = shop_etl.extract(SOURCE_CSV, tmp_path)
    daily = shop_etl.transform(orders, tmp_path)
    assert shop_etl.check(daily) == 8
    assert shop_etl.load(daily, tmp_path / "shop.duckdb") == 8

    with duckdb.connect(str(tmp_path / "shop.duckdb"), read_only=True) as con:
        rows = con.sql("SELECT order_date, orders, revenue FROM daily_revenue ORDER BY order_date").fetchall()
    # Order 106 is cancelled and order 109 has no amount, so 8 of the 10 orders count.
    assert rows[0] == (date(2026, 1, 10), 1, Decimal("9.00"))
    assert sum(revenue for _, _, revenue in rows) == Decimal("127.00")


def test_load_twice_gives_the_same_table(tmp_path):
    daily = shop_etl.transform(shop_etl.extract(SOURCE_CSV, tmp_path), tmp_path)
    shop_etl.load(daily, tmp_path / "shop.duckdb")
    assert shop_etl.load(daily, tmp_path / "shop.duckdb") == 8


def test_check_refuses_negative_revenue(tmp_path):
    bad = tmp_path / "bad.parquet"
    duckdb.execute(f"COPY (SELECT DATE '2026-01-01' AS order_date, 1 AS orders, -5.00 AS revenue) TO '{bad}' (FORMAT parquet)")
    with pytest.raises(ValueError, match="negative revenue"):
        shop_etl.check(bad)


def test_check_refuses_empty_input(tmp_path):
    empty = tmp_path / "empty.parquet"
    duckdb.execute(f"COPY (SELECT DATE '2026-01-01' AS order_date, 1 AS orders, 1.00 AS revenue WHERE false) TO '{empty}' (FORMAT parquet)")
    with pytest.raises(ValueError, match="empty"):
        shop_etl.check(empty)
