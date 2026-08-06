import requests

class FabricNotebookRuns:

    @staticmethod
    def build_notebook_execution_payload(
        driver_memory: str,
        driver_cores: int,
        executor_memory: str,
        executor_cores: int,
        num_executors: int,
        instance_pool_name: str | None = None,
        instance_pool_type: str = "Workspace"
    ) -> dict:
        """
        driver_memory: Must be one of ['28g', '56g', '112g']
        driver_cores: Must be one of [4, 8, 16]
        executor_memory: Must be one of ['28g', '56g', '112g']
        executor_cores: Must be one of [4, 8, 16]
        num_executors: Must be one of [2, 3, 4, 5]
        """

        compute_config = {
            "driverMemory": driver_memory,
            "driverCores": driver_cores,
            "executorMemory": executor_memory,
            "executorCores": executor_cores,
            "numExecutors": num_executors,
        }

        if instance_pool_name is not None:
            compute_config["instancePool"] = {
                "name": instance_pool_name,
                "type": instance_pool_type
            }

        return compute_config

    @staticmethod
    def post_run_notebook(workspace_id: str, notebook_id: str, api_token: str, req_payload: dict, beta='false') -> requests.Response:
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

    @staticmethod
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