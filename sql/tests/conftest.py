import sys
from pathlib import Path

import pytest

SQL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SQL_DIR))

from run_query import connect  # noqa: E402


@pytest.fixture
def run():
    """Run queries/<name> against a fresh in-memory copy of the shop data and return its rows."""
    con = connect()

    def _run(name: str) -> list[tuple]:
        return con.sql((SQL_DIR / "queries" / name).read_text()).fetchall()

    yield _run
    con.close()
