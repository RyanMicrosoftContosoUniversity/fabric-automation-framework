# test as class

import requests


class CustomPools:
    @staticmethod
    def _valid_node_sizes(node_size:str):
        node_size = node_size.lower()

        if node_size not in ('small', 'medium', 'large', 'xlarge', 'xxlarge'):
            raise ValueError(f"Invalid node size {node_size}.  Must be one of 'small', 'medium', 'large', 'xlarge', 'xxlarge'")

        node_map = {
            'small': 'Small',
            'medium': 'Medium',
            'large': 'Large',
            'xlarge': 'XLarge',
            'xxlarge': 'XXLarge'
        }

        return node_map[node_size]
    
    @staticmethod
    def _valid_autoscale(autoscale_dict:dict):
        if autoscale_dict['enabled'] not in ('true', 'false'):
            raise ValueError(f'Autoscale must be one of true or false, got: {autoscale_dict["enabled"]}')
        if autoscale_dict['minNodeCount'] > autoscale_dict['maxNodeCount']:
            raise ValueError(f'Autoscale minNodeCount must be less than maxNodeCount, got: {autoscale_dict}')

    @staticmethod
    def _valid_dynamicExecutorAllocation(dynamicExecutorAllocation_dict:dict):
        if dynamicExecutorAllocation_dict['enabled'] not in ('true', 'false'):
            raise ValueError(f'dynamicExecutorAllocation must be one of true or false, got: {dynamicExecutorAllocation_dict["enabled"]}')
        if dynamicExecutorAllocation_dict['minExecutors'] > dynamicExecutorAllocation_dict['maxExecutors']:
            raise ValueError(f'dynamicExecutorAllocation minExecutors must be less than maxExecutors, got: {dynamicExecutorAllocation_dict}')

    @staticmethod
    def create_custom_pool(workspace_id:str, api_token:str, pool_name:str, node_size:str, autoscale_dict:dict, dynamicExecutorAllocation_dict:dict):
        """
        Create Workspace Custom Pool
        https://learn.microsoft.com/en-us/rest/api/fabric/spark/custom-pools/create-workspace-custom-pool?tabs=HTTP
        POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools

        args:
            workspace_id:str: The guid of the workspace
            api_token:str: The api token to authenticate with the API

        """
        # validations
        node_size = CustomPools._valid_node_sizes(node_size)
        CustomPools._valid_autoscale(autoscale_dict)
        CustomPools._valid_dynamicExecutorAllocation(dynamicExecutorAllocation_dict)

        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        pool_payload = {
            "name": f"{pool_name}",
            "nodeFamily": "MemoryOptimized",
            "nodeSize": f"{node_size}",
            "autoScale": autoscale_dict,
            "dynamicExecutorAllocation": dynamicExecutorAllocation_dict
            }

        response = requests.post(url, headers=headers, json=pool_payload)

        return response

    @staticmethod
    def get_custom_pool(workspace_id:str, pool_id:str, api_token:str):
        """
        Get custom pool
        https://learn.microsoft.com/en-us/rest/api/fabric/spark/custom-pools/get-workspace-custom-pool?tabs=HTTP
        GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools/{poolId}

        args:
            workspace_id:str: The guid of the workspace
            pool_id:str:  The guid of the pool
            api_token:str: The token used to authenticate

        """
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools/{pool_id}'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }


        response = requests.get(url, headers=headers)

        return response

    @staticmethod
    def delete_custom_pool(workspace_id:str, pool_id:str, api_token:str):
        """
        Delete custom pool
        https://learn.microsoft.com/en-us/rest/api/fabric/spark/custom-pools/delete-workspace-custom-pool?tabs=HTTP
        DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools/{poolId}

        args:
            workspace_id:str: The guid of the workspace
            pool_id:str: The guid of the pool
            api_token:str: The token used to authenticate

        """
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools/{pool_id}'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        response = requests.delete(url, headers=headers)

        if response.status_code==200:
            print(f'INFO: Pool with id: {pool_id} successfully deleted')

        return response
    
    @staticmethod
    def list_custom_pools(workspace_id:str, api_token:str):
        """
        List custom pools
        https://learn.microsoft.com/en-us/rest/api/fabric/spark/custom-pools/list-workspace-custom-pools?tabs=HTTP
        GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools

        args:
            workspace_id:str: The guid of the workspace
            api_token:str: The token used to authenticate
        """
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)


        return response

    @staticmethod
    def update_custom_pool(workspace_id:str, api_token:str, pool_id:str, pool_name:str, node_size:str, autoscale_dict:dict, dynamicExecutorAllocation_dict:dict):
        """
        https://learn.microsoft.com/en-us/rest/api/fabric/spark/custom-pools/update-workspace-custom-pool?tabs=HTTP
        PATCH https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/spark/pools/{poolId}

        args:
            workspace_id:str: The guid of the workspace
            pool_id:str: The guid of the pool
            api_token:str: The token used to authenticate
        """
        # validations
        code_size = CustomPools._valid_node_sizes(node_size)
        CustomPools._valid_autoscale(autoscale_dict)
        CustomPools._valid_dynamicExecutorAllocation(dynamicExecutorAllocation_dict)

        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/spark/pools/{pool_id}'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        pool_payload = {
            "name": f"{pool_name}",
            "nodeFamily": "MemoryOptimized",
            "nodeSize": f"{node_size}",
            "autoScale": autoscale_dict,
            "dynamicExecutorAllocation": dynamicExecutorAllocation_dict
            }

        response = requests.patch(url, headers=headers, json=pool_payload)

        return response