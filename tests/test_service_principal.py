import pytest
from unittest.mock import patch, MagicMock
from fabric_automation_framework.service_principal import ServicePrincipal

@pytest.fixture
def mock_secret_client():
    with patch('fabric_automation_framework.service_principal.SecretClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.get_secret.return_value.value = "mock_client_secret"
        mock_client.return_value = mock_instance
        yield mock_client

@pytest.fixture
def mock_default_azure_credential():
    with patch('fabric_automation_framework.service_principal.DefaultAzureCredential') as mock_credential:
        yield mock_credential

@pytest.fixture
def mock_confidential_client_application():
    with patch('fabric_automation_framework.service_principal.msal.ConfidentialClientApplication') as mock_app:
        mock_instance = MagicMock()
        mock_instance.acquire_token_for_client.return_value = {'access_token': 'mock_access_token'}
        mock_app.return_value = mock_instance
        yield mock_app

def test_service_principal_init(mock_secret_client, mock_default_azure_credential, mock_confidential_client_application):
    client_id = "mock_client_id"
    tenant_id = "mock_tenant_id"
    spn_secret_name = "mock_secret_name"
    vault_url = "https://mock-vault-url"

    sp = ServicePrincipal(client_id, tenant_id, spn_secret_name, vault_url)

    # Verify SecretClient was called with correct parameters
    mock_secret_client.assert_called_once_with(vault_url=vault_url, credential=mock_default_azure_credential.return_value)
    mock_secret_client.return_value.get_secret.assert_called_once_with(spn_secret_name)

    # Verify ConfidentialClientApplication was initialized correctly
    mock_confidential_client_application.assert_called_once_with(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential="mock_client_secret"
    )

    # Verify access token was retrieved
    mock_confidential_client_application.return_value.acquire_token_for_client.assert_called_once_with(
        ['https://analysis.windows.net/powerbi/api/.default']
    )
    assert sp.access_token == "mock_access_token"