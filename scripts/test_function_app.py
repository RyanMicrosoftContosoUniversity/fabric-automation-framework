import logging
from fabric_utils.service_principal import ServicePrincipal
from fabric_utils.fabric_capacity import Extract, FabricCapacitiesBySubscription, FabricCapacityMGMT
import os


spn = ServicePrincipal(
    client_id='15a84224-c1e2-45e0-a2f5-fc8f5206f81d',
    tenant_id='35acf02c-4b87-4ae6-9221-ff5cafd430b4',
    spn_secret_name='spn-secret',
    vault_url='https://kvfabricprodeus2rh.vault.azure.net/'
)
subscription_id ='910ebf13-1058-405d-b6cf-eda03e5288d1'

client = FabricCapacitiesBySubscription(spn=spn, subscription_id=subscription_id, rg_name='fabric-rg')

caps_list = client.list_capacities_by_resource_group()

for item in caps_list:
    # create FabricCapacityMGMT so that the capacity can be paused
    id = Extract.extract_id(item)
    # get subscription_id
    subscription_id = Extract.extract_subscription_id(id)

    # get resource_group
    resource_group = Extract.extract_resource_group(id)

    # get capacity_name
    capacity_name = Extract.extract_capacity(id)

    
    print(item)

    # test values
    print(f'The value for subscription_id is {subscription_id}')
    print(f'The value for resource_group is {resource_group}')
    print(f'The value for capacity_name is {capacity_name}')

    # create FabricCapacityMGMT object
    capacity_client = FabricCapacityMGMT(spn=spn, subscription_id=subscription_id, resource_group=resource_group, capacity_name=capacity_name)

    # pause capacity
    # capacity_client.pause_capacity()

    # move up to next capacity
    # capacity_client.scale_up_capacity()

    # scale down capacity
    capacity_client.scale_down_capacity()
