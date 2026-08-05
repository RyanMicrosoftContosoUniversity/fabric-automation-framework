# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Token utilities: Azure Key Vault integration test
# 
# Retrieves service-principal settings through Fabric `notebookutils`, requests a Fabric API token through `Utils`, and validates safe JWT metadata. The notebook never displays secrets or the token.

# PARAMETERS CELL ********************

# Parameters - supply these values before running the integration test.
KV_URI = ""
CLIENT_ID_SECRET_NAME = ""
TENANT_ID_SECRET_NAME = ""
CLIENT_SECRET_NAME = ""
EXPECTED_AUDIENCE = "https://analysis.windows.net/powerbi/api"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import base64
import json
import time
from datetime import datetime, timezone

from fabric_utils.token_utils import Utils

required_parameters = {
    "KV_URI": KV_URI,
    "CLIENT_ID_SECRET_NAME": CLIENT_ID_SECRET_NAME,
    "TENANT_ID_SECRET_NAME": TENANT_ID_SECRET_NAME,
    "CLIENT_SECRET_NAME": CLIENT_SECRET_NAME,
}
missing_parameters = [name for name, value in required_parameters.items() if not value.strip()]
assert not missing_parameters, f"Set these notebook parameters before running: {', '.join(missing_parameters)}"
assert KV_URI.startswith("https://"), "KV_URI must be an HTTPS Azure Key Vault URI."

token = Utils.get_api_token_via_akv(
    KV_URI,
    CLIENT_ID_SECRET_NAME,
    TENANT_ID_SECRET_NAME,
    CLIENT_SECRET_NAME,
)

assert isinstance(token, str) and token, "Utils returned an empty or non-string token."
token_parts = token.split(".")
assert len(token_parts) == 3, "The returned access token is not a JWT."

payload = token_parts[1]
payload += "=" * (-len(payload) % 4)
claims = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))

audience = claims.get("aud")
audiences = audience if isinstance(audience, list) else [audience]
assert EXPECTED_AUDIENCE in audiences, f"Unexpected token audience: {audience!r}"

expires_at = claims.get("exp")
assert isinstance(expires_at, int), "The token has no numeric expiration claim."
assert expires_at > time.time() + 60, "The returned token is already expired or expires within one minute."

safe_result = {
    "audience": audience,
    "expires_at_utc": datetime.fromtimestamp(expires_at, timezone.utc).isoformat(),
    "tenant_id": claims.get("tid"),
    "application_id": claims.get("appid") or claims.get("azp"),
}
print("PASS: Key Vault secret retrieval and Fabric API token acquisition succeeded.")
print(json.dumps(safe_result, indent=2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
