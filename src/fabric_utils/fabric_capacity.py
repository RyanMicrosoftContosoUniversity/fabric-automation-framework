"""
Module for managing Fabric Capacities

Tasks
Create Capacity
Update Capacity
Delete Capacity
Get Capacity
List by Resource Group
List by Subscription
List SKUs
List SKUs for Capacity
Resume
Suspend
Update

"""
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.fabric import FabricMgmtClient
from .service_principal import ServicePrincipal
import json
import re
from azure.keyvault.secrets import SecretClient
import asyncio

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-fabric
# USAGE
    python fabric_capacities_create_or_update.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""

# define a global dict for all classes to use; setting hard max at F64
CAPACITY_LIST = [
    'F2',
    'F4',
    'F8',
    'F16',
    'F32',
    'F64'
]

class Extract:
    """
    Given a response like:
    {'properties': {'provisioningState': 'Succeeded', 'state': 'Paused', 'administration': {'members': ['admin@MngEnvMCAP372892.onmicrosoft.com']}}, 'id': '/subscriptions/910ebf13-1058-405d-b6cf-eda03e5288d1/resourceGroups/fabric-rg/providers/Microsoft.Fabric/capacities/fabricf2testrh', 'name': 'fabricf2testrh', 'type': 'Microsoft.Fabric/capacities', 'location': 'East US 2', 'sku': {'name': 'F2', 'tier': 'Fabric'}, 'tags': {}}
    extract subscription
    """
    def extract_id(subscription_response:dict):
        """
        {'properties': {'provisioningState': 'Succeeded', 'state': 'Paused', 'administration': {'members': ['admin@MngEnvMCAP372892.onmicrosoft.com']}}, 'id': '/subscriptions/910ebf13-1058-405d-b6cf-eda03e5288d1/resourceGroups/fabric-rg/providers/Microsoft.Fabric/capacities/fabricf2testrh', 'name': 'fabricf2testrh', 'type': 'Microsoft.Fabric/capacities', 'location': 'East US 2', 'sku': {'name': 'F2', 'tier': 'Fabric'}, 'tags': {}}
    extract id
        """
        id = subscription_response['id']
        return id


    def extract_subscription_id(id_string:str)->str:
        # Use regex to find the subscription id in the given string
        match = re.search(r'/subscriptions/([a-f0-9-]+)/', id_string)
        if match:
            return match.group(1)
        else:
            return None
        
    def extract_resource_group(id_string:str)->str:
        # Use regex to find the resource group in the given string
        match = re.search(r'/resourceGroups/([^/]+)/', id_string)
        if match:
            return match.group(1)
        else:
            return None
        
    def extract_capacity(id_string:str)->str:
        # Use regex to find the capacity in the given string
        match = re.search(r'/capacities/([^/]+)', id_string)
        if match:
            return match.group(1)
        else:
            return None


class FabricCapacitiesBySubscription:
    """
    Get all Fabric Capacities from a subscription
    """
    def __init__(self, spn:ServicePrincipal, subscription_id:str, rg_name:str):
        self.spn = spn
        self.subscription_id = subscription_id
        self.rg_name = rg_name
        self.client = FabricMgmtClient(
            credential=ClientSecretCredential(tenant_id=spn.tenant_id, client_id=spn.client_id, client_secret=spn.client_secret.value),
            subscription_id=self.subscription_id,
            base_url='https://management.azure.com'
        )
        self.capacities_list = self.list_capacities_by_resource_group()


    def list_capacities_by_resource_group(self)->list:
        
        # list be resource group name
        items = self.client.fabric_capacities.list_by_resource_group(resource_group_name=self.rg_name)
        capacities_list = [item for item in items]
        return capacities_list

class FabricCapacityMGMT:
    """
    This will be used to manage Fabric Capacities
    """
    def __init__(self, spn:ServicePrincipal, subscription_id:str, resource_group:str, capacity_name:str):
        self.spn = spn
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.capacity_name = capacity_name
        self.client = FabricMgmtClient(
            credential=ClientSecretCredential(tenant_id=spn.tenant_id, client_id=spn.client_id, client_secret=spn.client_secret.value),
            subscription_id=self.subscription_id
        )
        self.capacity_result = self._get_capacity()
 

    def _update_capacity_info(self, result):
        """
        """
        self.properties = result['properties']
        self.capacity_id = result['id']
        self.location = result['location']
        self.name = result['name']
        self.state = result.properties['state']
        self.sku_full = result['sku']
        self.sku = self.sku_full['name']
        self.admins = self.properties['administration']

    def _get_capacity(self)->json:
        """
        Use this to get metadata about the capacity, including state
        """
        response = self.client.fabric_capacities.get(
            resource_group_name=self.resource_group,
            capacity_name=self.capacity_name
        )

        # update capacity result
        self._update_capacity_info(response)

        return response
    
    def get_capacity(self):
        """
        """
        response = self.client.fabric_capacities.get(
            resource_group_name=self.resource_group,
            capacity_name=self.capacity_name
        )

        return response
    
    @staticmethod
    def get_next_sku(sku:str, change:int)->str:
        """
        Given a SKU, return the next SKU in the list
        """
        sku_index = CAPACITY_LIST.index(sku)
        if change > 0:
            if sku_index + 1 < len(CAPACITY_LIST):
                print(f'INFO: Next SKU: {CAPACITY_LIST[sku_index + 1]}')
                return CAPACITY_LIST[sku_index + 1]
            else:
                raise ValueError(f"ERROR: Current SKU: {sku}. No next SKU available")
        elif change < 0:
            if sku_index - 1 >= 0:
                print(f'INFO: Previous SKU: {CAPACITY_LIST[sku_index - 1]}')
                return CAPACITY_LIST[sku_index - 1]
            else:
                raise ValueError(f"ERROR: Current SKU: {sku}. No previous SKU available")
            

    def scale_up_capacity(self):
        """
        Update the capacity with new properties
        """
        if self.state == 'Paused':
            print(f'INFO: Capacity: {self.name} is paused. Cannot scale down')
            return
        
        next_sku = FabricCapacityMGMT.get_next_sku(self.sku, 1)

        self.client.fabric_capacities.begin_create_or_update(
            resource_group_name=self.resource_group,
            capacity_name=self.capacity_name,
            resource={
                'location': self.location,
                'properties': {
                    'administration': {
                        'members': self.admins['members']
                    }
                },
                'sku': {
                    'name': next_sku,
                    'tier': self.sku_full['tier']
                }
            }
        ).result()

    def scale_down_capacity(self):
        """
        Update the capacity with new properties
        """
        if self.state == 'Paused':
            print(f'INFO: Capacity: {self.name} is paused. Cannot scale down')
            return

        prev_sku = FabricCapacityMGMT.get_next_sku(self.sku, -1)

        self.client.fabric_capacities.begin_create_or_update(
            resource_group_name=self.resource_group,
            capacity_name=self.capacity_name,
            resource={
                'location': self.location,
                'properties': {
                    'administration': {
                        'members': self.admins['members']
                    }
                },
                'sku': {
                    'name': prev_sku,
                    'tier': self.sku_full['tier']
                }
            }
        ).result()

    def delete_capacity(self):
        """
        """
        pass

    def pause_capacity(self)->str:
        """
        """
        # check if capacity is already paused
        if self.state == 'Paused':
            print(f'Capacity: {self.name} is already paused')
            return self.state
        
        # pause capacity if not already paused
        self.client.fabric_capacities.begin_suspend(
            resource_group_name=self.resource_group,
            capacity_name=self.capacity_name
        ).result()

        # validate capacity paused
        cap_response = self.get_capacity()

        return cap_response['properties']['state']

    def resume_capacity(self):
        """
        """
        self.client.fabric_capacities.begin_resume(
            resource_group_name=self.resource_group,
            capacity_name=self.capacity_name
        ).result()

        # validate capacity resumed
        cap_response = self.get_capacity()

        return cap_response['properties']['state']





# def main():
#     client = FabricMgmtClient(
#         credential=DefaultAzureCredential(),
#         subscription_id="SUBSCRIPTION_ID",
#     )

#     response = client.fabric_capacities.begin_create_or_update(
#         resource_group_name="TestRG",
#         capacity_name="azsdktest",
#         resource={
#             "location": "westcentralus",
#             "properties": {"administration": {"members": ["azsdktest@microsoft.com", "azsdktest2@microsoft.com"]}},
#             "sku": {"name": "F2", "tier": "Fabric"},
#         },
#     ).result()
#     print(response)


# # x-ms-original-file: 2023-11-01/FabricCapacities_CreateOrUpdate.json
# if __name__ == "__main__":
#     main()


# quick tests

# get capacity
# client.get_capacity()

# resume capacity
# client.resume_capacity()