import os
import time
import msal

class Client:
    """Service principal client for Fabric / Power BI REST APIs.

    Credentials are read from the CLIENT_ID, TENANT_ID and CLIENT_SECRET
    Airflow environment variables unless passed explicitly.
    """

    POWERBI_SCOPE = ['https://analysis.windows.net/powerbi/api/.default']

    def __init__(self, client_id: str = None, tenant_id: str = None, client_secret: str = None,
                 scopes: list = None):
        self.client_id = client_id or os.environ.get('CLIENT_ID') or os.environ.get('AZURE_CLIENT_ID')
        self.tenant_id = tenant_id or os.environ.get('TENANT_ID') or os.environ.get('AZURE_TENANT_ID')
        self.scopes = scopes or self.POWERBI_SCOPE
        client_secret = client_secret or os.environ.get('CLIENT_SECRET') or os.environ.get('AZURE_CLIENT_SECRET')

        missing = [
            name for name, value in (
                ('CLIENT_ID', self.client_id),
                ('TENANT_ID', self.tenant_id),
                ('CLIENT_SECRET', client_secret),
            ) if not value
        ]
        if missing:
            raise ValueError(
                'Missing Airflow environment variables: ' + ', '.join(missing) +
                '. Set them under Settings > Environment configuration > Environment variables.'
            )

        self.authority = f'https://login.microsoftonline.com/{self.tenant_id}'
        self._access_token = None
        self._token_expiry = 0

        print(f'INFO: ServicePrincipal client initialized for tenant {self.tenant_id}')

        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=client_secret,
        )

    @classmethod
    def from_connection(cls, conn_id: str = 'fabric_spn', scopes: list = None):
        """Build a Client from an Airflow Connection.

        Credentials live Fernet-encrypted in the Airflow metadata DB, so nothing
        sensitive is stored in the item definition or committed to git.
        """
        from airflow.hooks.base import BaseHook

        conn = BaseHook.get_connection(conn_id)
        tenant_id = (
            conn.extra_dejson.get('tenant_id')
            or conn.extra_dejson.get('tenantId')
            or conn.extra_dejson.get('extra__azure__tenantId')
        )
        if not tenant_id:
            raise ValueError(
                f"Connection '{conn_id}' is missing a tenant id "
                "(expected 'tenant_id' or 'tenantId' in Extra)."
            )

        return cls(
            client_id=conn.login,
            tenant_id=tenant_id,
            client_secret=conn.password,
            scopes=scopes,
        )


    @staticmethod
    def _extract_token(result: dict) -> str:
        """MSAL returns an error dict rather than raising, so surface it explicitly."""
        if 'access_token' not in result:
            raise RuntimeError(
                f"Token request failed: {result.get('error')} - {result.get('error_description')}"
            )
        return result['access_token']

    def _acquire(self):
        result = self.app.acquire_token_for_client(self.scopes)
        self._access_token = self._extract_token(result)
        self._token_expiry = time.time() + result.get('expires_in', 3600)

    @property
    def access_token(self) -> str:
        """Client-credentials token, refreshed automatically 5 minutes before expiry."""
        if self._access_token is None or time.time() > (self._token_expiry - 300):
            self._acquire()
        return self._access_token

    def get_access_token(self, scopes: list = None) -> str:
        if scopes and scopes != self.scopes:
            return self._extract_token(self.app.acquire_token_for_client(scopes))
        return self.access_token

    def get_access_token_on_behalf_of(self, scopes, user_assertion) -> str:
        return self._extract_token(self.app.acquire_token_on_behalf_of(scopes, user_assertion))

    def get_access_token_by_authorization_code(self, scopes, code, redirect_uri) -> str:
        return self._extract_token(
            self.app.acquire_token_by_authorization_code(code, scopes, redirect_uri=redirect_uri)
        )

    def get_access_token_by_refresh_token(self, scopes, refresh_token) -> str:
        return self._extract_token(self.app.acquire_token_by_refresh_token(refresh_token, scopes))