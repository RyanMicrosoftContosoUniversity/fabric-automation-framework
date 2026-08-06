# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
# META   },
# META   "dependencies": {}
# META }

# MARKDOWN ********************

# Notebook to Trigger other Notebooks


# CELL ********************

import requests
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import os
import notebookutils
import pandas as pd
import time

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

def get_api_token_via_akv(kv_uri:str, client_id_secret:str, tenant_id_secret:str, client_secret_name:str)->str:
    """
    Function to retrieve an api token used to authenticate with Microsoft Fabric APIs

    kv_uri:str: The uri of the azure key vault
    client_id_secret:str: The name of the key used to store the value for the client id in the akv
    tenant_id_secret:str: The name of the key used to store the value for the tenant id in the akv
    client_secret_name:str: The name of the key used to store the value for the client secret in the akv

    """
    client_id = notebookutils.credentials.getSecret(kv_uri, client_id_secret)
    tenant_id = notebookutils.credentials.getSecret(kv_uri, tenant_id_secret)
    client_secret = notebookutils.credentials.getSecret(kv_uri, client_secret_name)

    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    scope = 'https://analysis.windows.net/powerbi/api/.default'
    token = credential.get_token(scope).token

    return token


def build_notebook_execution_payload(driver_memory:str, driver_cores:int, executor_memory:str, executor_cores:int, num_executors:int, instance_pool_name:str |None = None, instance_pool_type:str='Workspace'):
    """
    driver_memory:str:      Must be one of ['28g', '56g', '112g']
    driver_cores:int:       Must be one of [4,8,16]
    executor_memory:str:    Must be one of ['28g', '56g', '112g']
    executor_cores:int:     Must be one of [4,8,16]
    num_executors:int       Must be one of [2,3,4,5]
    """
    compute_config = {
         "driverMemory": driver_memory,
         "driverCores": driver_cores,
         "executorMemory": executor_memory,
         "executorCores": executor_cores,
         "numExecutors": num_executors,
     }

    if instance_pool_name is not None:
        compute_config['instancePool'] = {
            'name': instance_pool_name,
            'type': instance_pool_type
        }

    return {
         "executionData": {
             "compute": "Spark",
             "computeConfiguration": compute_config,
         }
     }


def post_run_notebook(workspace_id:str, notebook_id:str, api_token:str, req_payload:dict, beta='false')->requests.Response:
    """
    https://learn.microsoft.com/en-us/rest/api/fabric/notebook/background-jobs/run-on-demand-notebook?tabs=HTTP
    POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/notebooks/{notebookId}/jobs/execute/instances?beta={beta}

    set beta = 'false' to use the release version


    """
    url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/notebooks/{notebook_id}/jobs/execute/instances?beta={beta}'


    headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
    }    

    response = requests.post(url, headers=headers, json=req_payload)

    return response

def get_notebook_run_details(
    submission_response: requests.Response,
    api_token: str,
) -> dict:
    location = submission_response.headers["Location"]

    response = requests.get(
        location,
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=30,
    )

    print("HTTP:", response.status_code)
    print(response.text)
    response.raise_for_status()
    return response.json()



client = Client.client(client_id = client_id_secret,
     tenant_id = tenant_id_secret,
    spn_secret_name = client_secret_name,
    vault_url = kv_uri)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

kv_uri = 'https://kvfabricprodeus2rh.vault.azure.net/'
client_id_secret = 'fuam-spn-client-id'
tenant_id_secret = 'fuam-spn-tenant-id'
client_secret_name = 'fuam-spn-secret'

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# get oauth token
token = get_api_token_via_akv(kv_uri, client_id_secret, tenant_id_secret, client_secret_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

### Some tests
# https://app.powerbi.com/groups/896bca78-0d4a-4dc9-8716-05539ecf4ea5/synapsenotebooks/faf89dba-9ea9-4c83-b6e8-faca61764d2e?ctid=35acf02c-4b87-4ae6-9221-ff5cafd430b4&experience=power-bi

# fixed values
workspace_id = '896bca78-0d4a-4dc9-8716-05539ecf4ea5'
notebook_id = 'faf89dba-9ea9-4c83-b6e8-faca61764d2e'

# build payload
driver_memory = '28g'
driver_cores = 4
executor_memory = '56g'
executor_cores = 4
num_executors = 3
test_payload_1 = build_notebook_execution_payload(driver_memory, driver_cores, executor_memory, executor_cores, num_executors)

# execute notebook
res = post_run_notebook(workspace_id, notebook_id, token, req_payload=test_payload_1, beta='false')


# get response details
run_details = get_notebook_run_details(res, token)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# get response details
run_details = get_notebook_run_details(res, token)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# build payload for large pool
driver_memory = '112g'
driver_cores = 16
executor_memory = '112g'
executor_cores = 16
num_executors = 1
test_payload_2 = build_notebook_execution_payload(driver_memory, driver_cores, executor_memory, executor_cores, num_executors, instance_pool_name='large-pool', instance_pool_type='Workspace')

# execute notebook
res = post_run_notebook(workspace_id, notebook_id, token, req_payload=test_payload_2, beta='false')


# get response details
run_details = get_notebook_run_details(res, token)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# get response details
run_details = get_notebook_run_details(res, token)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# build payload f
res

# execute notebook

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

dir(time)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
