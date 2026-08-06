from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.keyvault.secrets import SecretClient

class Utils:
    @staticmethod
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