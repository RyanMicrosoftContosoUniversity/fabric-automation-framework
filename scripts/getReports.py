from src.service_principal import ServicePrincipal
from src.scan import Scan
import json
import time
import requests

class API_Utils:
    """
    This will be used to initiate a scan and hold all data that results from a scan
    Will require an SPN instance to authenticate
    """
    @staticmethod
    def getReport(spn:ServicePrincipal, groupId:str, reportId:str) -> dict:
        """
        https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}
        """
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {spn.access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get report: {response.status_code} {response.text}")
    
    @staticmethod
    def _buildReportsAsAdminFilter(workspace_list:list) -> str:
        """
        https://learn.microsoft.com/en-us/rest/api/power-bi/admin/reports-get-reports-as-admin
        GET https://api.powerbi.com/v1.0/myorg/admin/reports?$filter={$filter}&$top={$top}&$skip={$skip}

        Given a workspace list, build a filter string for the reports API
        EX: filter = "workspaceId eq a3b0108e-3e14-4064-b8ff-7c77eaf1a5d7"
        http://host/service/Products?$filter=Name in ('Milk', 'Cheese')
        """
        filter = " or ".join([f"workspaceId eq {workspace}" for workspace in workspace_list])
        return filter

    @staticmethod
    def getReportsAsAdmin(spn:ServicePrincipal, workspace_list:list=None) -> list:
        """
        GET https://api.powerbi.com/v1.0/myorg/admin/reports?$filter={$filter}&$top={$top}&$skip={$skip}
        https://api.powerbi.com/v1.0/myorg/admin/reports?$filter={filter}
        """
        if workspace_list is None:
            url = f"https://api.powerbi.com/v1.0/myorg/admin/reports"
        else:
            filter = API_Utils._buildReportsAsAdminFilter(workspace_list)
            url = f"https://api.powerbi.com/v1.0/myorg/admin/reports?$filter={filter}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {spn.access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['value']
        else:
            raise Exception(f"Failed to get reports: {response.status_code} {response.text}")

    @staticmethod
    def getReportUsersAsAdmin(spn:ServicePrincipal, reportId:str) -> list:
        """
        https://api.powerbi.com/v1.0/myorg/admin/reports/{reportId}/users
        """
        url = f"https://api.powerbi.com/v1.0/myorg/admin/reports/{reportId}/users"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {spn.access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['value']
        else:
            raise Exception(f"Failed to get report: {response.status_code} {response.text}")

workspace_list = [
    'a3b0108e-3e14-4064-b8ff-7c77eaf1a5d7',
    '35084d0d-db6d-4b37-91df-e9b9e329dd4f'
]
data_dict = {}

# base tests
config_data = json.loads(open('docs/non-prod-spn-config.json').read())
spn = ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
)
    

# get reports as admin
reports_list = API_Utils.getReportsAsAdmin(spn, workspace_list)

for report in reports_list:
    # get report users as admin
    report_users_resp = API_Utils.getReportUsersAsAdmin(spn, report['id'])

    # append to data_dict
    data_dict[report['id']] = {
        'name': report['name'],
        'users': report_users_resp
    }


# print(data_dict)

# write to file
with open('docs/report_users.json', 'w') as f:
    json.dump(data_dict, f, indent=4)




