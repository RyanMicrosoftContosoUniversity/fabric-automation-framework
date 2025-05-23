from src.service_principal import ServicePrincipal
import json
import time
import requests


class FabricDataPipelineRun:
    """
    This will be used to initiate a scan and hold all data that results from a scan
    Will require an SPN instance to authenticate
    """
    @staticmethod
    def run_on_demand_item_job(spn:ServicePrincipal, workspace_id:str, pipeline_id:str) -> dict:
        """
        https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{pipeline_id}/jobs/instances?jobType=Pipeline
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{pipeline_id}/jobs/instances?jobType=Pipeline"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {spn.access_token}'
        }

        body = {
            "executionData": {
                "parameters": {
                    "param_waitsec": "10"
                }
            }
        }


        response = requests.post(url, headers=headers, data=json.dumps(body))
        if response.status_code in (200, 202):
            return response.headers['Location']
        else:
            raise Exception(f"Failed to get pipeline run: {response.status_code} {response.text}")
        
    @staticmethod
    def get_jobid_from_job_url(url:str) -> str:
        """
        Given a job URL, extract the job ID from it.

        Example Input: https://api.fabric.microsoft.com/v1/workspaces/c0a7b8a9-eb12-495a-b863-2cb583e31154/items/114cad78-70c4-4c85-8d16-7e5210f9231d/jobs/instances/78bffa7f-f539-409f-a64b-f837084c68fb
        Output: 78bffa7f-f539-409f-a64b-f837084c68fb
        """
        # Split the URL by slashes and get the last segment
        job_id = url.split('/')[-1]
        return job_id

    @staticmethod
    def refresh_token(func):
        """
        Decorator to refresh the access token if it is about to expire.
        """
        def wrapper(self, *args, **kwargs):
            self.check_and_refresh_token()
            return func(self, *args, **kwargs)
        return wrapper

    @refresh_token
    @staticmethod
    def check_job_status(spn:ServicePrincipal, workspace_id:str, pipeline_id:str, job_id:str) -> dict:
        """
        Check the status of a job given its ID.
        https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/jobs/instances/{jobId}
        https://api.fabric.microsoft.com/v1/workspaces/<your WS Id>/items/<pipeline id>/jobs/instances/<job ID>
        """
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{pipeline_id}/jobs/instances/{job_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {spn.access_token}'
        }

        response = requests.get(url, headers=headers)
        if response.status_code in (200, 202):
            return response.json()
        else:
            raise Exception(f"Failed to get job status: {response.status_code} {response.text}")
        
