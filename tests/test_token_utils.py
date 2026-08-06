import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, call, patch


MODULE_PATH = (
    Path(__file__).parents[1] / "src" / "fabric_utils" / "token_utils.py"
)
SPEC = importlib.util.spec_from_file_location("token_utils", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
token_utils = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(token_utils)
Utils = token_utils.Utils


def test_get_api_token_via_akv_uses_fabric_secrets_to_request_token():
    get_secret = MagicMock(
        side_effect=["client-id", "tenant-id", "client-secret"]
    )
    notebookutils = SimpleNamespace(
        credentials=SimpleNamespace(getSecret=get_secret)
    )
    credential = MagicMock()
    credential.get_token.return_value.token = "fabric-token"

    with (
        patch.object(
            token_utils,
            "notebookutils",
            notebookutils,
            create=True,
        ),
        patch.object(
            token_utils,
            "ClientSecretCredential",
            return_value=credential,
        ) as credential_class,
    ):
        token = Utils.get_api_token_via_akv(
            "https://example.vault.azure.net/",
            "client-id-secret",
            "tenant-id-secret",
            "client-secret-name",
        )

    assert token == "fabric-token"
    assert get_secret.call_args_list == [
        call("https://example.vault.azure.net/", "client-id-secret"),
        call("https://example.vault.azure.net/", "tenant-id-secret"),
        call("https://example.vault.azure.net/", "client-secret-name"),
    ]
    credential_class.assert_called_once_with(
        "tenant-id",
        "client-id",
        "client-secret",
    )
    credential.get_token.assert_called_once_with(
        "https://analysis.windows.net/powerbi/api/.default"
    )
