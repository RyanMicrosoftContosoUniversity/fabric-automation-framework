"""
This module will be used for table objects within the metadata database
This will take results from the scan and create tables in the metadata database
"""


class workspace_table:
    """
    This class will be used to create the workspace table
    """
    def __init__(self, id:str, name:str, type:str, isOnDedicatedCapacity:bool, capacityId:str, defaultDatasetStorageFormat:str, reports:list=None)
        self.id = id
        self.name = name
        self.type = type
        self.isOnDedicatedCapacity = isOnDedicatedCapacity
        self.capacityId = capacityId
        self.defaultDatasetStorageFormat = defaultDatasetStorageFormat
        self.reports = reports



class report_table:
    """
    This class will be used to create the report table
    """
    def __init__(self, id:str, workspaceId:str, name:str, datasetId:str, createdDateTime:str, modifiedDateTime:str, modifiedBy:str, endorsementDetails:dict, sensitivityLabel:dict, users:list):
        self.id = id
        self.workspaceId = workspaceId
        self.name = name
        self.datasetId = datasetId
        self.createdDateTime = createdDateTime
        self.modifiedDateTime = modifiedDateTime
        self.modifiedBy = modifiedBy
        self.endorsementDetails = endorsementDetails
        self.sensitivityLabel = sensitivityLabel
        self.users = users



class dataflow_table:
    """
    This class will be used to create the dataflow table
    """
    def __init__(self, objectId:str, workspaceId:str, name:str, description:str, configuredBy:str, modifiedBy:str, 
                 modifiedDateTime:str, endorsementDetails:dict, datasourceUsages:list,
                   misconfiguredDatasourceUsages:list, sensitivityLabel:dict, users:list):
        self.objectId = objectId
        self.workspaceId = workspaceId
        self.name = name
        self.description = description
        self.configuredBy = configuredBy
        self.modifiedBy = modifiedBy
        self.modifiedDateTime = modifiedDateTime
        self.endorsementDetails = endorsementDetails
        self.datasourceUsages = datasourceUsages
        self.misconfiguredDatasourceUsages = misconfiguredDatasourceUsages
        self.sensitivityLabel = sensitivityLabel
        self.users = users



class dashboard_table:
    """
    This class will be used to create the dashboard table
    """
    def __init__(self, id:str, workspaceId:str, isReadOnly:bool, titles:list, sensitivityLabel:dict, users:list):
        self.id = id
        self.workspaceId = workspaceId
        self.isReadOnly = isReadOnly
        self.titles = titles
        self.sensitivityLabel = sensitivityLabel
        self.users = users


class workspace_users_table:
    """
    This class will be used to create the workspace users table
    """
    def __init__(self, displayName:str, workspaceId:str, emailAddress:str, appUserAccessRight:str,
                 identifier:str, graphId:str, principalType:str):
        self.displayName = displayName
        self.workspaceId = workspaceId
        self.emailAddress = emailAddress
        self.appUserAccessRight = appUserAccessRight
        self.identifier = identifier
        self.graphId = graphId
        self.principalType = principalType



class datamart_table:
    """
    This class will be used to create the dataamrt table
    """
    def __init__(self, id:str, workspaceId:str, name:str, description:str, type:str, configuredBy:str,
                 configuredById:str, modifiedBy:str, modifiedDateTime:str, sensitivityLabel:dict,
                 endorseentDetails:dict, upstreamDataflows:list, datasourceUsages:list, users:list):
        pass


class dataset_table:
    """
    This class will be used to create the dataset table
    """
    def __init__(self, id:str, workspaceId:str, tables:list, relationships:list,
                 configuredBy:str, endorsementDetails:dict, expressions:list, roles:list,
                 uptreamDataflows:list, datasourceUsages:list, sensitivityLabel:dict, users:list):
        self.id = id
        self.workspaceId = workspaceId
        self.tables = tables
        self.relationships = relationships
        self.configuredBy = configuredBy
        self.endorsementDetails = endorsementDetails
        self.expressions = expressions
        self.roles = roles
        self.uptreamDataflows = uptreamDataflows
        self.datasourceUsages = datasourceUsages
        self.sensitivityLabel = sensitivityLabel
        self.users = users
        
