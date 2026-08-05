# Fabric notebook source


# MARKDOWN ********************

# # Token utilities: Fabric runtime smoke tests
# 
# Validates that the Fabric runtime exposes `notebookutils` and that the packaged `fabric_utils.token_utils.Utils` class can be imported.

# PARAMETERS CELL ********************

# Parameters
EXPECTED_MODULE = "fabric_utils.token_utils"

# CELL ********************

import importlib

assert "notebookutils" in globals(), "Fabric did not inject notebookutils into the notebook runtime."
assert hasattr(notebookutils, "credentials"), "notebookutils.credentials is unavailable."
assert callable(notebookutils.credentials.getSecret), "notebookutils.credentials.getSecret is unavailable."

token_utils = importlib.import_module(EXPECTED_MODULE)
assert hasattr(token_utils, "Utils"), f"{EXPECTED_MODULE} does not expose Utils."
assert callable(token_utils.Utils.get_api_token_via_akv), "Utils.get_api_token_via_akv is unavailable."

print("PASS: Fabric runtime and token utility import checks succeeded.")
