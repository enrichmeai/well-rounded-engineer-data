# One task, three data libraries

The same small job written three times, in [pandas](https://github.com/pandas-dev/pandas),
[Polars](https://github.com/pola-rs/polars) and [DuckDB](https://github.com/duckdb/duckdb):
**revenue per customer per month** from 200 shop orders.

Read first: [Data libraries in the guide](https://enrichmeai.com/well-rounded-engineer/datalibs/).

## What it shows

- `revenue.py` has three functions, one per library, that follow the same rules: leave out cancelled
  orders, leave out orders with no amount yet, group by customer and month, round to 2 decimal places.
- `tests/test_revenue.py` checks that all three give exactly the same answer, from a CSV file and from a
  Parquet file, and that the answer matches a fourth version written with nothing but Python's `csv` module.
- It also shows a real difference between the libraries: the sum of a group whose values are **all missing**.
  pandas and Polars say `0`; DuckDB follows SQL and says `NULL` (unknown). That is why `revenue.py` decides the
  rule (drop missing amounts) before summing, instead of leaving it to whichever library runs the code.
- `data/orders.csv` was made by `make_data.py` with a fixed random seed, so it is the same every time.

## Run it

You need Python 3.11 or newer. From inside this `datalibs/` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

python revenue.py data/orders.csv  # print the result from each library
pytest                             # 3 tests
```

## Which one to pick

There is no winner: they are good at different things.

- **pandas** is the one most tutorials, notebooks and other libraries expect. Pick it when you are working
  with code or people that already use it, or when another library wants a pandas DataFrame. It runs each step
  straight away (eagerly) and keeps the whole table in memory.
- **Polars** has a lazy mode: `scan_csv(...)` builds a plan, and nothing is read until `collect()`, so it can
  skip columns and rows it does not need. Pick it for new Python data code where you want speed and a strict,
  consistent API. Note that its `group_by` does not promise an output order, so sort when order matters.
- **DuckDB** lets you write SQL directly over CSV and Parquet files, with no load step. Pick it when the
  logic is easiest to say in SQL, or when the same query should also run in a database or in dbt.

All three read and write Parquet, and DuckDB can query a pandas or Polars DataFrame by name, so mixing them in
one project is normal.

## Try this

1. Add a fourth rule: leave out orders with status `placed` too. Change all three functions, and keep the test green.
2. Change the task to revenue **per month only** (all customers together). Which version needed the fewest changes?
3. Run `python make_data.py` with 200 changed to 2,000,000, then time each function. Which is fastest on your laptop?
   (Put the 200 back before you commit, or the tests will fail: they expect the small file.)

## Read next

- [Data libraries in the guide](https://enrichmeai.com/well-rounded-engineer/datalibs/)
- The SQL behind the DuckDB version, one idea at a time: [`../sql/`](../sql/)
