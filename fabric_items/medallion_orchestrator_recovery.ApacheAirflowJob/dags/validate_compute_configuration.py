"""Manual validation DAG for SQL-driven Fabric notebook compute sizing."""

from datetime import datetime, timedelta

from airflow import DAG
from fabric_notebook_fallback import (
    SqlConfiguredFabricNotebookOperator,
)

WORKSPACE_ID = "896bca78-0d4a-4dc9-8716-05539ecf4ea5"
PROBE_NOTEBOOK_ID = "ab554b94-8a42-406c-9c4b-13f12270206c"


with DAG(
    dag_id="validate_compute_configuration",
    description="Manually validate SQL-driven Fabric Spark compute sizing",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    is_paused_upon_creation=True,
    default_args={
        "owner": "data-engineering",
        "retries": 0,
        "execution_timeout": timedelta(minutes=60),
    },
    tags=["fabric", "medallion", "validation"],
) as dag:
    SqlConfiguredFabricNotebookOperator(
        task_id="probe_effective_compute_configuration",
        fabric_conn_id="fabric_conn",
        sql_conn_id="airflow_config_sql",
        workspace_id=WORKSPACE_ID,
        notebook_id=PROBE_NOTEBOOK_ID,
    )
