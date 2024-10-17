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

## Example
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



## Setup

    1. Create App Registration 

Search for 'App Registration' in Azure Portal
Create New Registration

![Alt text](docs\images\App_Registration_1.png)


Assuming this will be done for a single AD/Entra Tenant, select Single tenant:
![Alt text](docs\images\App_Registration_2.png)



Redirect URI is not necessary



    2. Create an Azure Key Vault
        a. This will be utilized to store the SPN secret when it is created




    3. Navigate back to App Registrations and create a Client Secret
![Alt text](docs\images\App_Registration_3.png)
    


This client secret will be stored in the Azure Key Vault just created to retrieve the secret at runtime to get an oauth token to authenticate with the API Endpoints



Under API Permissions, add Tenant.Read.All from the Power BI Service:
![Alt text](docs\images\App_Registration_4.png)

NOTE: Do not change Admin Consent Required to No as this will cause issues with the scanner endpoints




    4. Create Security Groups

Search for 'Microsoft Entra' in the Azure Portal and select Groups:
![Alt text](docs\images\Security_Groups_5.png)


Create a new group of type 'Security' and add the SPN(s) created to the group:
![Alt text](docs\images\Security_Groups_6.png)




    5. Enable Power BI Tenant Settings
Navigate to the Power BI Admin Portal Tenant Settings

Enable 'Service principals can use Fabric APIs for Specific Security Groups and add the group(s) you created:
![Alt text](docs\images\Tenant_Settings_7.png)



Do the same for 'Service principals can access read-only admin APIs', 'Enhance admin APIs responses with detailed mnetadata' and 'Enhance admin APIs responses with DAX and mashup expressions'
![Alt text](docs\images\Tenant_Settings_8.png)
![Alt text](docs\images\Tenant_Settings_9.png)
![Alt text](docs\images\Tenant_Settings_10.png)









Access the POC Code:

    1. Navigate to fabric-automation-framework - Repos (azure.com)
    2. Clone the code in local git
![Alt text](docs\images\POC_11.png)
    3. Pip install the poc code:
![Alt text](docs\images\POC_12.png)
    4. Adjust the configuration file: docs\non-prod-spn-config.json to reflect your resources
![Alt text](docs\images\POC_12.png)


To test locally, run the script at: scripts\metadata_scan.py to write the scan files to the local docs folder:
![Alt text](docs\images\POC_13.png)



To perform ETL on the scan result, see the ipynb file here: scripts\process_metadata_scan.ipynb
