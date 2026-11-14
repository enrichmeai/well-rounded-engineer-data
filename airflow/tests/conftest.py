import os
import sys
import tempfile
from pathlib import Path

DAGS_DIR = Path(__file__).resolve().parents[1] / "dags"

# Keep Airflow's files (config, logs, the SQLite metadata database) out of your home folder.
# These must be set before anything imports airflow.
_airflow_home = tempfile.mkdtemp(prefix="airflow-home-")
os.environ.setdefault("AIRFLOW_HOME", _airflow_home)
os.environ.setdefault("AIRFLOW__CORE__LOAD_EXAMPLES", "False")
os.environ.setdefault("AIRFLOW__CORE__DAGS_FOLDER", str(DAGS_DIR))
os.environ.setdefault("SHOP_ETL_DIR", str(Path(_airflow_home) / "output"))

# Airflow puts the DAGs folder on sys.path when it parses DAGs; do the same so tests can import shop_etl.
sys.path.insert(0, str(DAGS_DIR))
