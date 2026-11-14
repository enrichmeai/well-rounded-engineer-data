"""Run one SQL file against the shop data and print the result.

Usage, from inside the sql/ folder:
    python run_query.py queries/05_row_number.sql
"""

import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent


def connect() -> duckdb.DuckDBPyConnection:
    """An in-memory DuckDB database with the shop tables loaded from data/."""
    con = duckdb.connect()
    # setup.sql uses paths relative to this folder, so point DuckDB's file search there.
    con.execute(f"SET file_search_path = '{HERE}'")
    con.execute((HERE / "setup.sql").read_text())
    return con


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    con = connect()
    con.sql(Path(sys.argv[1]).read_text()).show(max_rows=50)


if __name__ == "__main__":
    main()
