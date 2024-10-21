"""
Test file for performing etl on scan results
"""
import json
import src.table as table   


source_file = 'docs\scan_response.json'

with open(source_file, 'r') as f:
    data = json.load(f)

# handle file workspaces -- ignore datasourceInstances and isconfiguredDatasourceInstances for now
for workspace in data['workspaces']:
    # create workspace object
    try:
        default_ds_storage_format = workspace['defaultDatasetStorageFormat']
    except:
        default_ds_storage_format = None
    try:
        capacity_id = workspace['capacityId']
    except:
        capacity_id = None
    try:
        users = workspace['users']
    except:
        users = None    

    workspace_table = table.Workspace_table(name=workspace['name'], id=workspace['id'], type=workspace['type'], 
                                            isOnDedicatedCapacity=workspace['isOnDedicatedCapacity'],
                                            defaultDatasetStorageFormat=default_ds_storage_format, 
                                            capacityId=capacity_id,
                                            reports=workspace['reports'], dashboards=workspace['dashboards'],
                                            dataflows=workspace['dataflows'], datamarts=workspace['datamarts'], 
                                            datasets=workspace['datasets'], users=users)
