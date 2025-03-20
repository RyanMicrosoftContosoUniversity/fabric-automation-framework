import msal
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests

import json

class ServicePrincipal:
    def __init__(self, client_id:str, tenant_id:str, spn_secret_name:str, vault_url:str):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.spn_secret_name = spn_secret_name
        self.vault_url = vault_url

        print(f'INFO: created ServicePrincipal object for {self.client_id} with tenant {self.tenant_id}, authority {self.authority}, spn_secret_name {self.spn_secret_name}, vault_url {self.vault_url}')

        self.client_secret = self._get_spn_secret(self.spn_secret_name, self.vault_url)
        self.app = msal.ConfidentialClientApplication(
            self.client_id, authority=self.authority,
            client_credential=self.client_secret.value
        )
        self.access_token = self.get_access_token(['https://analysis.windows.net/powerbi/api/.default'])

        

    def _get_spn_secret(self, secret_name, vault_url):
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        return secret

    def get_access_token(self, scopes):
        result = self.app.acquire_token_for_client(scopes)
        return result['access_token']

    def get_access_token_on_behalf_of(self, scopes, user_assertion):
        result = self.app.acquire_token_on_behalf_of(scopes, user_assertion)
        return result['access_token']

    def get_access_token_by_authorization_code(self, scopes, code, redirect_uri):
        result = self.app.acquire_token_by_authorization_code(code, scopes, redirect_uri=redirect_uri)
        return result['access_token']

    def get_access_token_by_refresh_token(self, scopes, refresh_token):
        result = self.app.acquire_token_by_refresh_token(refresh_token, scopes)
        return result['access_token']
    

    