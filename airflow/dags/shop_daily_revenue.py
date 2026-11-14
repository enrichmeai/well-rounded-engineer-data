"""An Airflow 3 DAG: extract the shop's orders, work out revenue per day, check it, and load it.

Each task is a small Python function. The work itself lives in shop_etl.py; this file only says what
runs and in which order. Tasks pass file paths to each other (as strings), never the data itself:
what one task returns is stored by Airflow as an XCom, which is meant for small values.
"""

import os
from datetime import datetime, timezone
from pathlib import Path

from airflow.sdk import dag, task

import shop_etl

HERE = Path(__file__).resolve().parent
SOURCE_CSV = HERE.parent / "data" / "orders.csv"
# Where the pipeline writes its files. Override it with SHOP_ETL_DIR, as the tests do.
OUT_DIR = Path(os.environ.get("SHOP_ETL_DIR", HERE.parent / "output"))


@dag(
    schedule="@daily",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["well-rounded-engineer", "example"],
)
def shop_daily_revenue():
    @task
    def extract() -> str:
        return str(shop_etl.extract(SOURCE_CSV, OUT_DIR))

    @task
    def transform(orders_parquet: str) -> str:
        return str(shop_etl.transform(Path(orders_parquet), OUT_DIR))

    @task
    def check(daily_revenue_parquet: str) -> str:
        shop_etl.check(Path(daily_revenue_parquet))
        return daily_revenue_parquet

    @task
    def load(daily_revenue_parquet: str) -> int:
        return shop_etl.load(Path(daily_revenue_parquet), OUT_DIR / "shop.duckdb")

    # Calling the tasks like functions wires them together: extract >> transform >> check >> load.
    load(check(transform(extract())))


shop_daily_revenue()
