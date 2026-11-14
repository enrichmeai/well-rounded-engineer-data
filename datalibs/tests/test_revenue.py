import csv
from collections import defaultdict
from pathlib import Path

import duckdb
import pandas as pd
import polars as pl
import pytest

from revenue import revenue_duckdb, revenue_pandas, revenue_polars, rows

ORDERS_CSV = Path(__file__).resolve().parents[1] / "data" / "orders.csv"


def plain_python(path: Path) -> list[tuple[int, str, float]]:
    """A fourth answer with no data library at all, from the standard library's csv module."""
    totals: dict[tuple[int, str], float] = defaultdict(float)
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            if row["status"] == "cancelled" or row["amount"] == "":
                continue
            totals[(int(row["customer_id"]), row["order_date"][:7])] += float(row["amount"])
    return [(c, m, round(total, 2)) for (c, m), total in sorted(totals.items())]


@pytest.fixture(scope="module")
def orders_parquet(tmp_path_factory) -> Path:
    path = tmp_path_factory.mktemp("data") / "orders.parquet"
    duckdb.execute("COPY (SELECT * FROM read_csv($csv)) TO '" + str(path) + "' (FORMAT parquet)", {"csv": str(ORDERS_CSV)})
    return path


def test_all_three_libraries_agree_on_csv():
    expected = plain_python(ORDERS_CSV)
    assert len(expected) == 36  # 12 customers x 3 months, every pair has at least one counted order
    assert rows(revenue_pandas(ORDERS_CSV)) == expected
    assert rows(revenue_polars(ORDERS_CSV)) == expected
    assert rows(revenue_duckdb(ORDERS_CSV)) == expected


def test_all_three_libraries_agree_on_parquet(orders_parquet):
    expected = plain_python(ORDERS_CSV)
    assert rows(revenue_pandas(orders_parquet)) == expected
    assert rows(revenue_polars(orders_parquet)) == expected
    assert rows(revenue_duckdb(orders_parquet)) == expected


def test_libraries_disagree_on_the_sum_of_only_missing_values():
    """Why revenue.py drops missing amounts before summing: the libraries do not agree on this case.

    pandas and Polars say the sum of nothing-but-missing is 0. DuckDB follows SQL and says NULL
    (unknown). Neither is wrong, but compare them without deciding the rule first and they differ.
    """
    pandas_sum = pd.DataFrame({"k": [1, 1], "v": [None, None]}, dtype="float64").groupby("k")["v"].sum()
    polars_sum = (
        pl.DataFrame({"k": [1, 1], "v": [None, None]}, schema={"k": pl.Int64, "v": pl.Float64})
        .group_by("k")
        .agg(pl.col("v").sum())
    )
    duckdb_sum = duckdb.sql("SELECT k, sum(v) FROM (VALUES (1, NULL::DOUBLE), (1, NULL::DOUBLE)) AS t(k, v) GROUP BY k")

    assert pandas_sum.tolist() == [0.0]
    assert polars_sum["v"].to_list() == [0.0]
    assert duckdb_sum.fetchall() == [(1, None)]
