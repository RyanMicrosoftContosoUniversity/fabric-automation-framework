from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


credential = DefaultAzureCredential()
client = SecretClient(vault_url='https://kvfabricprodeus2rh.vault.azure.net/', credential=credential)
secret = client.get_secret('fake-secret')


print(f'Secret Value: {secret.value}')