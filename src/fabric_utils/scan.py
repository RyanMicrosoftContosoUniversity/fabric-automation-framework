import requests
import json
from .service_principal import ServicePrincipal


class Scan:
    """
    This will be used to initiate a scan and hold all data that results from a scan
    Will require an SPN instance to authenticate
    """
    def __init__(self, spn:ServicePrincipal, modified_since=None, exclude_personal_workspaces=True, exclude_inactive_workspaces=False):
        self.spn = spn
        self.modified_since = modified_since
        self.exclude_personal_workspaces = exclude_personal_workspaces
        self.exclude_inactive_workspaces = exclude_inactive_workspaces

        # initiate the scan
        self.get_modified_workspaces()
        self.scan_request = self.post_workspace_info(workspace_list=self.workspace_json_list)
        

    def get_modified_workspaces(self)->list:
        """
        modified_since: str: Last modified date and time in UTC. The format is 'YYYY-MM-DDTHH:MM:SSZ'.
        exclude_personal_workspaces: bool: Exclude personal workspaces.
        exclude_inactive_workspaces: bool: Exclude inactive workspaces.

        return list: ModifiedWorkspace: List of workspaces that have been modified.
        """
        if self.modified_since==None and self.exclude_personal_workspaces==True and self.exclude_inactive_workspaces==False:
            
            url = f'https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified?excludePersonalWorkspaces={self.exclude_personal_workspaces}'
        else:
            pass

        response = requests.get(url, headers={'Authorization': f'Bearer {self.spn.access_token}'})

        # pass to create_workspace_json_list method to create a list of workspaces
        self.workspaces_list = self.create_workspace_json_list(response.json())
        return response.json()
    
    def create_workspace_json_list(self, workspace_list:json)->json:
        """
        Creates a list of workspaces to be passed to the post_workspace_info method
        """
        workspace_json_list = {
            "workspaces": []
        }

        for item in workspace_list:
            value = item['id']
            workspace_json_list['workspaces'].append(value)

        self.workspace_json_list = workspace_json_list


    def post_workspace_info(self, workspace_list:list, dataset_expressions:bool=None, 
                            dataset_schema:bool=None, datasource_details:bool=None,
                            get_artifact_users:bool=None, lineage:bool=None):
        """
        Initiates a call to receive metadata for the requested list of workspaces
        dataset_expressions: bool: Whether to return dataset expressions (DAX and Mashup queries)
        dataset_schema: bool: Whether to return dataset schema(tables, columns, measures)
        datasource_details: bool: Whether to return datasource details (connection string, credential details)
        get_artifact_users: bool: Whether to return uer details for a Power BI item (report, dashboard)
        lineage: bool: Whether to return lineage information for a dataset
        """
        if dataset_expressions==None and dataset_schema==None and datasource_details==None and get_artifact_users==None and lineage==None:
            url = 'https://api.powerbi.com/v1.0/myorg/admin/workspaces/getInfo'
        else:  
            pass

        response = requests.post(url, headers={'Authorization': f'Bearer {self.spn.access_token}', 'Content-Type': 'application/json'}, json=workspace_list)

        return response.json()
    
    def get_scan_status(self, scan_id:str)->json:
        """
        Gets the scan status for the specified scan

        return json: ScanStatus: The status of the scan
        """
        url = f'https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanStatus/{scan_id}'

        response = requests.get(url, headers={'Authorization': f'Bearer {self.spn.access_token}'})

        if response.json()['status'] == 'Succeeded':
            return 'Succeeded'
        else:
            print('INFO: Scan has not completed successfully')
            return 'inProgress'


        return response.json()

    def get_scan_result(self, scan_id:str)->json:
        """
        Gets the scan results for the specified scan
        """
        url = f'https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanResult/{scan_id}'

        response = requests.get(url, headers={'Authorization': f'Bearer {self.spn.access_token}'})

        self.scan_results = response.json()

        return response.json()

        