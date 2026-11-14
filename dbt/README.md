# dbt on DuckDB

A small [dbt](https://github.com/dbt-labs/dbt-core) project for the same online shop as [`../sql/`](../sql/),
running on [dbt-duckdb](https://github.com/duckdb/dbt-duckdb). The warehouse is a single local DuckDB file,
so there is no account, no server and no credentials.

Read first: [dbt in the guide](https://enrichmeai.com/well-rounded-engineer/dbt/).

## What it shows

```
seeds/raw_*.csv  ->  models/staging/stg_*  ->  models/marts/fct_orders  ->  models/marts/dim_customers
   (raw data)        (rename, cast, clean)      (one row per order)          (one row per customer)
```

- **Seeds**: three small CSV files that dbt loads as tables, with their column types stated in `dbt_project.yml`.
- **Staging models** (views): one per source table, only renaming, casting and cleaning.
- **Mart models** (tables): `fct_orders` decides once what counts as revenue (not cancelled, has an amount),
  and `dim_customers` builds on it, keeping customers who have never ordered.
- **Data tests** on the real data, in the `_*.yml` files: `unique`, `not_null`, `relationships` (every order's
  customer and product exists) and `accepted_values` (the order status is one we know). Plus one singular test,
  `tests/assert_revenue_is_not_negative.sql`: any row it returns is a failure.
- **A unit test** (in `models/marts/_marts.yml`): it runs `dim_customers` on a few rows written by hand and checks
  the logic, before the model is built on real data. Unit tests arrived in dbt Core 1.8; this project uses 1.12.
- `profiles.yml` sits inside the project and points at `shop.duckdb` next to it, so nothing is written to your
  home folder.

## Run it

You need Python 3.11 or newer. From inside this `dbt/` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd shop
dbt build --profiles-dir .         # seeds, models and tests, in dependency order
```

The last line should read `Done. PASS=27 WARN=0 ERROR=0 SKIP=0 ...`. To look at the result:

```bash
python -c "import duckdb; duckdb.connect('shop.duckdb').sql('SELECT * FROM dim_customers').show()"
```

`cd ..` and run `pytest` to run `dbt build` into a temporary folder and check the finished `dim_customers`
table against answers worked out by hand (2 tests).

When you run dbt, it prints a note that dbt v2 is available. This project uses dbt Core 1.x with the dbt-duckdb
adapter, which is what the commands above install.

## Try this

1. Add `'returned'` to the order statuses in `seeds/raw_orders.csv` without changing the YAML. Run `dbt build`:
   which test fails, and what does dbt skip because of it?
2. Add a `customer_monthly_revenue` mart that builds on `fct_orders`, with a `not_null` test on its revenue column.
3. Break the unit test on purpose: change `dim_customers` to `sum(amount)` and run `dbt build --select dim_customers`.
   Read how dbt shows the difference between actual and expected.
4. Run `dbt docs generate --profiles-dir .` and then `dbt docs serve --profiles-dir .` to browse the lineage graph.

## Read next

- [dbt in the guide](https://enrichmeai.com/well-rounded-engineer/dbt/)
- The SQL ideas the models use: [`../sql/`](../sql/)
- Running a pipeline on a schedule: [`../airflow/`](../airflow/)
