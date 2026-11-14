# Well Rounded Engineer: data

Working with data: SQL, database design, data libraries, dbt and Airflow, on your laptop.

This repository holds small, runnable examples for the free guide
[Well Rounded Engineer — More Human](https://enrichmeai.com/well-rounded-engineer/). Every concept in the guide
links to a folder here, and every folder can be run on a laptop, with no cloud account and no paid tools.

## How it is organised

| Folder | What it shows | Read first |
|---|---|---|
| [`sql/`](sql/) | SQL skills | [guide](https://enrichmeai.com/well-rounded-engineer/sql/) |
| [`database/`](database/) | Database design | [guide](https://enrichmeai.com/well-rounded-engineer/database/) |
| [`datalibs/`](datalibs/) | Data libraries | [guide](https://enrichmeai.com/well-rounded-engineer/datalibs/) |
| [`dbt/`](dbt/) | dbt | [guide](https://enrichmeai.com/well-rounded-engineer/dbt/) |
| [`airflow/`](airflow/) | Airflow DAGs | [guide](https://enrichmeai.com/well-rounded-engineer/dags/) |

Each folder has its own README: what it shows, how to run it, what to try next, and what to read. Each example has
tests, and CI runs them on every change, so the code here keeps working.

Folders are added one pull request at a time. `database/` is planned and has no content yet.

Every folder is set up the same way: from inside it, create a virtual environment, install its pinned
`requirements.txt`, and run `pytest`. The folder's README has the exact commands.

## Why this exists

A click is cheaper than a prompt. For what is already known, read the guide and run the example; use AI where it
earns its keep. Read [why this guide exists](https://enrichmeai.com/well-rounded-engineer/why/).

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
