import json
from datetime import datetime

from airflow import DAG, settings
from airflow.hooks.base import BaseHook
from airflow.models import Connection
from airflow.operators.python import PythonOperator

TARGET_CONN_ID = "airflow_config_sql"


def upsert_connection():
    source = BaseHook.get_connection("fabric_conn")
    session = settings.Session()
    try:
        target = session.query(Connection).filter(Connection.conn_id == TARGET_CONN_ID).one_or_none()
        if target is None:
            target = Connection(conn_id=TARGET_CONN_ID)
        target.conn_type = "generic"
        target.host = "ftykynmhjpteverb75ok7vbqwq-pdfgxckkbxeu3bywavjz5t2ouu.database.fabric.microsoft.com"
        target.schema = "airflow_config-8c3d270b-c9d6-468a-b1bc-0c99059616de"
        target.login = source.login
        target.password = source.password
        target.port = None
        target.extra = json.dumps({
            "tenantId": "35acf02c-4b87-4ae6-9221-ff5cafd430b4",
            "driver": "ODBC Driver 18 for SQL Server",
            "token_scope": "https://database.windows.net/.default",
        })
        session.add(target)
        session.commit()
        print("Created or updated airflow_config_sql without emitting credentials")
    finally:
        session.close()


with DAG(
    dag_id="__setup_airflow_config_sql_once",
    schedule_interval="@once",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1,
) as dag:
    PythonOperator(task_id="upsert_connection", python_callable=upsert_connection)