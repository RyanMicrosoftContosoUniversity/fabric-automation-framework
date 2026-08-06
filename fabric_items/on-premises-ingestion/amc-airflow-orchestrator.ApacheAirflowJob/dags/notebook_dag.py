from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from client import Client
from fabric_notebook_runs import FabricNotebookRuns

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

### variables
workspace_id = '896bca78-0d4a-4dc9-8716-05539ecf4ea5'
notebook_id = 'faf89dba-9ea9-4c83-b6e8-faca61764d2e'


def task_python_notebook(**context):

    # credentials come from the CLIENT_ID / TENANT_ID / CLIENT_SECRET env vars
    client = Client.from_connection('fabric_spn')

    # create payload
    driver_memory = '28g'
    driver_cores = 4
    executor_memory = '56g'
    executor_cores = 4
    num_executors = 5
    payload = FabricNotebookRuns.build_notebook_execution_payload(
        driver_memory, driver_cores, executor_memory, executor_cores, num_executors
    )

    # execute notebook
    res = FabricNotebookRuns.post_run_notebook(
        workspace_id, notebook_id, client.access_token, req_payload=payload, beta='false'
    )

    # get response details
    run_details = FabricNotebookRuns.get_notebook_run_details(res, client.access_token)

    return run_details


# Instantiate the DAG object
with DAG(
    'dags-notebook_dag.py',
    default_args=default_args,
    description='A simple Hello World DAG',
    schedule_interval=None,
    catchup=False
) as dag:

    # Define the tasks
    hello_task = BashOperator(
        task_id='hello_world_task',
        bash_command='echo "Hello, World!"'
    )

    # Python  task
    run_notebook_task = PythonOperator(
        task_id='run_fabric_notebook_task',
        python_callable=task_python_notebook,
    )

    # Set the task dependencies
    hello_task >> run_notebook_task