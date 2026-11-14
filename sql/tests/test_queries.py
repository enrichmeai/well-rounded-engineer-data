"""Each test runs one file from queries/ and checks the exact answer, worked out by hand from data/."""

from datetime import date, datetime
from decimal import Decimal


def test_inner_join_returns_every_order_and_drops_customers_without_orders(run):
    rows = run("01_inner_join.sql")
    assert len(rows) == 10
    assert rows[0] == (101, "Asha", "Notebook", Decimal("9.00"))
    assert "Ema" not in {customer for _, customer, _, _ in rows}


def test_left_join_keeps_customers_without_orders(run):
    assert run("02_left_join.sql") == [
        ("Asha", 4),
        ("Ben", 3),
        ("Chloe", 2),
        ("Dev", 1),
        ("Ema", 0),
    ]


def test_anti_join_finds_products_never_ordered(run):
    assert run("03_anti_join.sql") == [("Headphones",)]


def test_having_filters_groups_after_aggregation(run):
    # Ben (6.00) and Dev (18.00) are under 30; Ben's cancelled 25.00 is removed by WHERE first.
    assert run("04_group_by_having.sql") == [
        ("Asha", 4, Decimal("54.00")),
        ("Chloe", 2, Decimal("49.00")),
    ]


def test_row_number_picks_each_customers_first_order(run):
    assert run("05_row_number.sql") == [
        (1, 101, date(2026, 1, 10)),
        (2, 103, date(2026, 1, 28)),
        (3, 104, date(2026, 2, 3)),
        (4, 107, date(2026, 2, 21)),
    ]


def test_running_total_per_customer_skips_nulls(run):
    spent = [(customer, order, total) for customer, order, _, _, total in run("06_running_total.sql")]
    assert spent == [
        (1, 101, Decimal("9.00")),
        (1, 102, Decimal("34.00")),
        (1, 105, Decimal("42.00")),
        (1, 110, Decimal("54.00")),
        (2, 103, Decimal("6.00")),
        (2, 109, Decimal("6.00")),  # amount is NULL, so the total does not move
        (3, 104, Decimal("24.00")),
        (3, 108, Decimal("49.00")),
        (4, 107, Decimal("18.00")),
    ]


def test_lag_gives_days_since_previous_order(run):
    days = [(order, gap) for _, order, _, _, gap in run("07_lag.sql")]
    assert days == [
        (101, None),
        (102, 15),
        (105, 20),
        (110, 23),
        (103, None),
        (106, 18),
        (109, 18),
        (104, None),
        (108, 27),
        (107, None),
    ]


def test_qualify_keeps_latest_email_per_customer(run):
    assert run("08_dedupe_qualify.sql") == [
        (1, "asha.k@example.com", datetime(2026, 2, 10, 12, 0)),
        (2, "ben@example.com", datetime(2026, 1, 17, 10, 0)),
        (3, "chloe.m@example.com", datetime(2026, 3, 1, 11, 15)),
        (4, "dev@example.com", datetime(2026, 2, 20, 16, 45)),
    ]


def test_null_behaviour(run):
    assert run("09_null_behaviour.sql") == [
        (10, 9, Decimal("152.00"), 16.89, 15.2, None, True, None),
    ]


def test_not_equal_silently_drops_null_rows(run):
    assert run("10_null_comparison_trap.sql") == [("Ben", "US"), ("Ema", "DE")]


def test_is_distinct_from_keeps_null_rows(run):
    assert run("11_null_comparison_fix.sql") == [("Ben", "US"), ("Dev", None), ("Ema", "DE")]
