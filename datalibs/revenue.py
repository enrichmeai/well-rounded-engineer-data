"""Revenue per customer per month, written three times: pandas, Polars and DuckDB.

The rules are the same in all three:
- cancelled orders do not count;
- orders with no amount yet (NULL / missing) do not count;
- month is the order date as 'YYYY-MM';
- revenue is the sum of amount, rounded to 2 decimal places;
- the result is sorted by customer_id, then month.

Each function returns the library's own kind of table. `rows()` turns any of them into a plain list of
(customer_id, month, revenue) tuples, so the three can be compared exactly.

Usage, from inside the datalibs/ folder:
    python revenue.py data/orders.csv
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd
import polars as pl


def _is_parquet(path: str | Path) -> bool:
    return Path(path).suffix == ".parquet"


def revenue_pandas(path: str | Path) -> pd.DataFrame:
    # pandas reads the whole file into memory, then each step makes a new DataFrame (eager).
    if _is_parquet(path):
        orders = pd.read_parquet(path)
        orders["order_date"] = pd.to_datetime(orders["order_date"])
    else:
        orders = pd.read_csv(path, parse_dates=["order_date"])
    orders = orders[(orders["status"] != "cancelled") & orders["amount"].notna()]
    orders = orders.assign(month=orders["order_date"].dt.strftime("%Y-%m"))
    result = (
        orders.groupby(["customer_id", "month"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "revenue"})
    )
    result["revenue"] = result["revenue"].round(2)
    return result.sort_values(["customer_id", "month"], ignore_index=True)


def revenue_polars(path: str | Path) -> pl.DataFrame:
    # Polars builds a lazy query plan from scan_*, optimises it, and runs it on collect().
    orders = pl.scan_parquet(path) if _is_parquet(path) else pl.scan_csv(path, try_parse_dates=True)
    return (
        orders.filter(pl.col("status") != "cancelled", pl.col("amount").is_not_null())
        .group_by(
            pl.col("customer_id"),
            pl.col("order_date").cast(pl.Date).dt.strftime("%Y-%m").alias("month"),
        )
        .agg(pl.col("amount").sum().round(2).alias("revenue"))
        # group_by does not promise an order, so sort explicitly.
        .sort("customer_id", "month")
        .collect()
    )


def revenue_duckdb(path: str | Path) -> duckdb.DuckDBPyRelation:
    # DuckDB runs SQL directly over the file: no load step, and nothing is read until you fetch.
    reader = "read_parquet" if _is_parquet(path) else "read_csv"
    return duckdb.sql(
        f"""
        SELECT
            customer_id,
            strftime(CAST(order_date AS DATE), '%Y-%m') AS month,
            round(sum(amount), 2)                       AS revenue
        FROM {reader}($path)
        WHERE status <> 'cancelled'
          AND amount IS NOT NULL
        GROUP BY ALL
        ORDER BY customer_id, month
        """,
        params={"path": str(path)},
    )


def rows(result: pd.DataFrame | pl.DataFrame | duckdb.DuckDBPyRelation) -> list[tuple[int, str, float]]:
    """Plain Python tuples, so results from different libraries compare with ==."""
    if isinstance(result, pd.DataFrame):
        raw = result.itertuples(index=False, name=None)
    elif isinstance(result, pl.DataFrame):
        raw = result.iter_rows()
    else:
        raw = result.fetchall()
    return [(int(c), str(m), float(r)) for c, m, r in raw]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    print("pandas:\n", revenue_pandas(path), "\n", sep="")
    print("Polars:\n", revenue_polars(path), "\n", sep="")
    print("DuckDB:")
    revenue_duckdb(path).show()


if __name__ == "__main__":
    main()
