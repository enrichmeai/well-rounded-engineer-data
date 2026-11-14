"""The ETL steps, as plain Python functions with no Airflow in them.

Keeping the work out of the DAG file means you can test it with plain pytest, and the DAG file stays
a short description of what runs in which order.
"""

from pathlib import Path

import duckdb


def extract(source_csv: Path, out_dir: Path) -> Path:
    """Copy the raw orders CSV into a Parquet file, with the types stated, so later steps read typed data."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "orders.parquet"
    with duckdb.connect() as con:
        con.execute(
            f"""
            COPY (
                SELECT *
                FROM read_csv(
                    '{source_csv}',
                    header = true,
                    columns = {{
                        'order_id': 'INTEGER', 'customer_id': 'INTEGER', 'product_id': 'INTEGER',
                        'order_date': 'DATE', 'quantity': 'INTEGER', 'amount': 'DECIMAL(10, 2)',
                        'status': 'VARCHAR'
                    }}
                )
            ) TO '{target}' (FORMAT parquet)
            """
        )
    return target


def transform(orders_parquet: Path, out_dir: Path) -> Path:
    """Revenue per day: cancelled orders and orders with no amount yet are left out."""
    target = out_dir / "daily_revenue.parquet"
    with duckdb.connect() as con:
        con.execute(
            f"""
            COPY (
                SELECT order_date, count(*) AS orders, sum(amount) AS revenue
                FROM '{orders_parquet}'
                WHERE status <> 'cancelled' AND amount IS NOT NULL
                GROUP BY order_date
                ORDER BY order_date
            ) TO '{target}' (FORMAT parquet)
            """
        )
    return target


def check(daily_revenue_parquet: Path) -> int:
    """Fail loudly instead of loading bad data: there must be rows, and no day may have negative revenue."""
    with duckdb.connect() as con:
        rows, negative = con.execute(
            f"SELECT count(*), count(*) FILTER (WHERE revenue < 0) FROM '{daily_revenue_parquet}'"
        ).fetchone()
    if rows == 0:
        raise ValueError("daily revenue is empty: refusing to load nothing")
    if negative:
        raise ValueError(f"{negative} day(s) have negative revenue")
    return rows


def load(daily_revenue_parquet: Path, database: Path) -> int:
    """Replace the daily_revenue table in a local DuckDB file. Running it twice gives the same table."""
    with duckdb.connect(str(database)) as con:
        con.execute(f"CREATE OR REPLACE TABLE daily_revenue AS SELECT * FROM '{daily_revenue_parquet}'")
        return con.execute("SELECT count(*) FROM daily_revenue").fetchone()[0]
