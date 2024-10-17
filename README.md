# Fabric Automation Framework
Note that this project is for POC purposes only.  Please see DISCLAIMER.md for more detials

A framework for automating tasks in a fabric environment.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Fabric Automation Framework is designed to simplify and automate various tasks within a fabric environment. It provides a set of tools and scripts to manage and interact with different components of the fabric infrastructure.

## Features

- **Service Principal Management**: Easily manage service principals and their secrets.
- **Workspace Management**: Automate the creation and modification of workspaces.
- **Configuration Management**: Load and manage configuration data from JSON files.

## Installation

To install the Fabric Automation Framework, clone the repository and install the dependencies:

```sh
git clone https://github.com/yourusername/fabric-automation-framework.git
cd fabric-automation-framework
pip install -e 
```

## Usage
Running the Metadata Scan Script
The metadata_scan.py script is used to scan and retrieve metadata for modified workspaces. To run the script, use the following command:

```
python -m scripts.metadata_scan
```

Example
Here's an example of how to use the ServicePrincipal class in your own scripts:
```
from src import service_principal
import json

config_data = json.loads(open('docs/non-prod-spn-config.json').read())
spn = service_principal.ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
)

modified_workspaces_list = spn.get_modified_workspaces()
print(modified_workspaces_list)
```


