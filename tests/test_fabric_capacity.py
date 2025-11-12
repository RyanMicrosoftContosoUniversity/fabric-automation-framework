import pytest
from fabric_utils.service_principal import ServicePrincipal
from fabric_utils.fabric_capacity import Extract, FabricCapacitiesBySubscription, FabricCapacityMGMT
from dotenv import load_dotenv
import os
load_dotenv()

# create a service principal object
# spn = ServicePrincipal(client_id=os.getenv('CLIENT_ID'), tenant_id=os.getenv('TENANT_ID'), spn_secret_name=os.getenv('SPN_SECRET_NAME'), vault_url=os.getenv('VAULT_URL'))

def test_valid_resource_group():
    id_string = "/subscriptions/12345/resourceGroups/my-resource-group/providers/Microsoft.Fabric/capacities/my-capacity"
    expected = "my-resource-group"
    result = Extract.extract_resource_group(id_string)
    assert result == expected

def test_no_resource_group():
    id_string = "/subscriptions/12345/providers/Microsoft.Fabric/capacities/my-capacity"
    result = Extract.extract_resource_group(id_string)
    assert result is None

def test_empty_string():
    id_string = ""
    result = Extract.extract_resource_group(id_string)
    assert result is None

def test_invalid_format():
    id_string = "invalid-string-without-resource-group"
    result = Extract.extract_resource_group(id_string)
    assert result is None

def test_list_capacities_by_resource_group(mocker):
    # Mock the ServicePrincipal and FabricMgmtClient
    mock_spn = mocker.Mock()
    mock_spn.tenant_id = os.getenv('TENANT_ID')
    mock_spn.client_id = os.getenv('CLIENT_ID')
    mock_spn.client_secret.value = os.getenv('SPN_SECRET_NAME')

    mock_subscription_id = os.getenv('SUBSCRIPTION_ID')
    mock_rg_name = os.getenv('RESOURCE_GROUP')

    # Mock the FabricMgmtClient and its list_by_resource_group method
    mock_client = mocker.patch("fabric_utils.fabric_capacity.FabricMgmtClient")
    mock_client_instance = mock_client.return_value
    mock_client_instance.fabric_capacities.list_by_resource_group.return_value = [
        {"name": "capacity1"},
        {"name": "capacity2"},
    ]

    # Instantiate the class and call the method
    fabric_capacities = FabricCapacitiesBySubscription(mock_spn, mock_subscription_id, mock_rg_name)
    result = fabric_capacities.list_capacities_by_resource_group()

    # Assertions
    assert len(result) == 2
    assert result[0]["name"] == "capacity1"
    assert result[1]["name"] == "capacity2"
    mock_client_instance.fabric_capacities.list_by_resource_group.assert_any_call(
    resource_group_name=mock_rg_name
)
    

def test_pause_capacity_already_paused(mocker):
    # Mock the ServicePrincipal and FabricMgmtClient
    mock_spn = mocker.Mock()
    mock_spn.tenant_id = os.getenv('TENANT_ID')
    mock_spn.client_id = os.getenv('CLIENT_ID')
    mock_spn.client_secret.value = os.getenv('SPN_SECRET_NAME')

    mock_subscription_id = os.getenv('SUBSCRIPTION_ID')
    mock_rg_name = os.getenv('RESOURCE_GROUP')
    mock_capacity_name = "test-capacity"

    # Mock the FabricMgmtClient and its methods
    mock_client = mocker.patch("fabric_utils.fabric_capacity.FabricMgmtClient")
    mock_client_instance = mock_client.return_value
    mock_client_instance.fabric_capacities.get.return_value = {
        "properties": {"state": "Paused"}
    }

    # Instantiate the class
    fabric_capacity_mgmt = FabricCapacityMGMT(mock_spn, mock_subscription_id, mock_rg_name, mock_capacity_name)

    # Call the pause_capacity method
    result = fabric_capacity_mgmt.pause_capacity()

    # Assertions
    assert result == "Paused"
    mock_client_instance.fabric_capacities.get.assert_called_with(
        resource_group_name=mock_rg_name,
        capacity_name=mock_capacity_name
    )

def test_pause_capacity_not_paused(mocker):
    # Mock the ServicePrincipal and FabricMgmtClient
    mock_spn = mocker.Mock()
    mock_spn.tenant_id = os.getenv('TENANT_ID')
    mock_spn.client_id = os.getenv('CLIENT_ID')
    mock_spn.client_secret.value = os.getenv('SPN_SECRET_NAME')

    mock_subscription_id = os.getenv('SUBSCRIPTION_ID')
    mock_rg_name = os.getenv('RESOURCE_GROUP')
    mock_capacity_name = "test-capacity"

    # Mock the FabricMgmtClient and its methods
    mock_client = mocker.patch("fabric_utils.fabric_capacity.FabricMgmtClient")
    mock_client_instance = mock_client.return_value
    mock_client_instance.fabric_capacities.get.side_effect = [
        {"properties": {"state": "Running"}},  # Initial state
        {"properties": {"state": "Paused"}}   # After pausing
    ]
    mock_client_instance.fabric_capacities.begin_suspend.return_value.result.return_value = None

    # Instantiate the class
    fabric_capacity_mgmt = FabricCapacityMGMT(mock_spn, mock_subscription_id, mock_rg_name, mock_capacity_name)

    # Call the pause_capacity method
    result = fabric_capacity_mgmt.pause_capacity()

    # Assertions
    assert result == "Paused"
    mock_client_instance.fabric_capacities.begin_suspend.assert_called_with(
        resource_group_name=mock_rg_name,
        capacity_name=mock_capacity_name
    )

def test_resume_capacity(mocker):
    # Mock the ServicePrincipal and FabricMgmtClient
    mock_spn = mocker.Mock()
    mock_spn.tenant_id = os.getenv('TENANT_ID')
    mock_spn.client_id = os.getenv('CLIENT_ID')
    mock_spn.client_secret.value = os.getenv('SPN_SECRET_NAME')

    mock_subscription_id = os.getenv('SUBSCRIPTION_ID')
    mock_rg_name = os.getenv('RESOURCE_GROUP')
    mock_capacity_name = "test-capacity"

    # Mock the FabricMgmtClient and its methods
    mock_client = mocker.patch("fabric_utils.fabric_capacity.FabricMgmtClient")
    mock_client_instance = mock_client.return_value
    mock_client_instance.fabric_capacities.get.side_effect = [
        {"properties": {"state": "Paused"}},  # Initial state
        {"properties": {"state": "Running"}}  # After resuming
    ]
    mock_client_instance.fabric_capacities.begin_resume.return_value.result.return_value = None

    # Instantiate the class
    fabric_capacity_mgmt = FabricCapacityMGMT(mock_spn, mock_subscription_id, mock_rg_name, mock_capacity_name)

    # Call the resume_capacity method
    result = fabric_capacity_mgmt.resume_capacity()

    # Assertions
    assert result == "Running"
    mock_client_instance.fabric_capacities.begin_resume.assert_called_with(
        resource_group_name=mock_rg_name,
        capacity_name=mock_capacity_name
    )

    

