"""
This module will be used for table objects within the metadata database
This will take results from the scan and create tables in the metadata database
"""

class EndorsementDetails:
    """
    This class will be used to create the endorsementDetails table
    """
    def __init__(self, fk_object_id:str, foreignKeyObjectType:str, endorsement:str, certifiedBy:str):
        fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType
        self.endorsement = endorsement
        self.certifiedBy = certifiedBy

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['report', 'dataflow', 'datamart', 'dataset']:
            raise ValueError('foreignKeyObjectType must be one of the following: report, dataflow, datamart, dataset')
        
class Table:
    """
    This class will be used to create the table table
    """
    def __init__(self, name:str, fk_dataset_id:str):
        self.name = name
        self.fk_dataset_id = fk_dataset_id



class Expression:
    """
    This class will be used to create the expression table
    """
    def __init__(self, name:str, fk_dataset_id:str, description:str, expression:str):
        self.name = name
        self.fk_dataset_id = fk_dataset_id
        self.description = description
        self.expression = expression

class UpstreamDataflow:
    """
    This class will be used to create the upstream_dataflow table
    """
    def __init__(self, targetDataflowId:str, groupId:str, fk_object_id:str, foreignKeyObjectType:str):
        self.targetDataflowId = targetDataflowId
        self.groupId = groupId
        self.fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['dataflow', 'dataset']:
            raise ValueError('foreignKeyObjectType must be one of the following: dataflow, dataset')
        
class Role:
    """
    This class will be used to create the role table
    """
    def __init__(self, name:str, modelPermission:str, fk_dataset_id:str):
        self.name = name
        self.modelPermission = modelPermission
        self.fk_dataset_id = fk_dataset_id

class DatasourceUsage:
    """
    This class will be used to create the datasource_usage table
    """
    def __init__(self, datasourceInstanceId:str, fk_object_id:str, foreignKeyObjectType:str):
        self.datasourceInstanceId = datasourceInstanceId
        self.fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['dataflow', 'dataset']:
            raise ValueError('foreignKeyObjectType must be one of the following: dataflow, dataset')

class SensitivityLabel:
    """
    This class will be used to create the sensitivityLabel table
    """
    def __init__(self, labelId:str, fk_object_id:str, foreignKeyObjectType:str):
        self.labelId = labelId
        fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['report', 'dataflow', 'datamart', 'dataset']:
            raise ValueError('foreignKeyObjectType must be one of the following: report, dataflow, datamart, dataset')

class User:
    """
    This class will be used to create the user table
    """
    def __init__(self, displayName:str, fk_object_id:str, foreignKeyObjectType:str, emailAddress:str, appUserAccessRight:str, identifier:str, graphId:str, principalType:str, userType:str, profile:dict):
        self.displayName = displayName
        self.fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType
        self.emailAddress = emailAddress
        self.appUserAccessRight = appUserAccessRight
        self.identifier = identifier
        self.graphId = graphId
        self.principalType = principalType

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['workspace', 'report', 'dataflow', 'dataset']:
            raise ValueError('foreignKeyObjectType must be one of the following: workspace, report, dataflow, dataset')


class Workspace_table:
    """
    This class will be used to create the workspace table
    """
    def __init__(self, id:str, name:str, type:str, isOnDedicatedCapacity:bool, capacityId:str, 
                 defaultDatasetStorageFormat:str, reports:list=None, dashboards:list=None, dataflows:list=None,
                 datamarts:list=None, datasets:list=None, users:list=None):
        self.id = id
        self.name = name
        self.type = type
        self.isOnDedicatedCapacity = isOnDedicatedCapacity
        self.capacityId = capacityId
        self.defaultDatasetStorageFormat = defaultDatasetStorageFormat
        self.reports = reports
        self.dashboards = dashboards
        self.dataflows = dataflows
        self.datamarts = datamarts
        self.datasets = datasets
        self.users = users

        # process reports
        for report in self.reports:
            report_table = Report_table(id=report['id'], workspaceId=self.id, name=report['name'],
                                        datasetId=report['datasetId'], createdDateTime=report['createdDateTime'],
                                        modifiedDateTime=report['modifiedDateTime'], modifiedBy=report['modifiedBy'],
                                        endorsementDetails=report['endorsementDetails'], sensitivityLabel=report['sensitivityLabel'],
                                        users=report['users'])

        # process dashboards
        for dashboard in self.dashboards:
            dashboard_table = Dashboard_table(id=dashboard['id'], workspaceId=self.id, isReadOnly=dashboard['isReadOnly'],
                                              tiles=dashboard['tiles'], sensitivityLabel=dashboard['sensitivityLabel'],
                                              users=dashboard['users'])

        # process dataflows
        for dataflow in self.dataflows:
            dataflow_table = Dataflow_table(objectId=dataflow['objectId'], workspaceId=self.id, name=dataflow['name'],
                                            description=dataflow['description'], configuredBy=dataflow['configuredBy'], modifiedBy=dataflow['modifiedBy'],
                                            modifiedDateTime=dataflow['modifiedDateTime'], endorsementDetails=dataflow['endorsementDetails'],
                                            datasourceUsages=dataflow['datasourceUsages'], misconfiguredDatasourceUsages=dataflow['misconfiguredDatasourceUsages'],
                                            sensitivityLabel=dataflow['sensitivityLabel'], users=dataflow['users'])    

        # process datamarts
        for datamart in self.datamarts:
            datamart_table = Datamart_table(id=datamart['id'], workspaceId=self.id, name=datamart['name'],
                                            description=datamart['description'], type=datamart['type'], configuredBy=datamart['configuredBy'],
                                            configuredById=datamart['configuredById'], modifiedBy=datamart['modifiedBy'], modifiedDateTime=datamart['modifiedDateTime'],
                                            sensitivityLabel=datamart['sensitivityLabel'], endorsementDetails=datamart['endorsementDetails'],
                                            upstreamDataflows=datamart['UpstreamDataflows'], datasourceUsages=datamart['datasourceUsages'], users=datamart['Users'])

        # process datasets
        for dataset in self.datasets:
            dataset_table = Dataset_table(id=dataset['id'], workspaceId=self.id, tables=dataset['tables'], relationships=dataset['relationships'],
                                          configuredBy=dataset['configuredBy'], endorsementDetails=dataset['endorsementDetails'], expressions=dataset['expressions'],
                                          roles=dataset['roles'], uptreamDataflows=dataset['upstreamDataflows'], datasourceUsages=dataset['datasourceUsages'],
                                          sensitivityLabel=dataset['sensitivityLabel'], users=dataset['users'])
        # process users
        if self.users!=None:
            for user in self.users:
                workspace_users_table = Workspace_users_table(displayName=user['displayName'], workspaceId=self.id, emailAddress=user['emailAddress'],
                                                            appUserAccessRight=user['appUserAccessRight'], identifier=user['identifier'], graphId=user['graphId'],
                                                            principalType=user['principalType'])


class Report_table:
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



class Dataflow_table:
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



class Dashboard_table:
    """
    This class will be used to create the dashboard table
    """
    def __init__(self, id:str, workspaceId:str, isReadOnly:bool, tiles:list, sensitivityLabel:dict, users:list):
        self.id = id
        self.workspaceId = workspaceId
        self.isReadOnly = isReadOnly
        self.tiles = tiles
        self.sensitivityLabel = sensitivityLabel
        self.users = users


class Workspace_users_table:
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



class Datamart_table:
    """
    This class will be used to create the dataamrt table
    """
    def __init__(self, id:str, workspaceId:str, name:str, description:str, type:str, configuredBy:str,
                 configuredById:str, modifiedBy:str, modifiedDateTime:str, sensitivityLabel:dict,
                 endorsementDetails:dict, upstreamDataflows:list, datasourceUsages:list, users:list):
        pass


class Dataset_table:
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

        # process tables
        for table in self.tables:
            my_table = Table(name=table['name'], fk_dataset_id=self.id)

        # process relationships
        for relationship in self.relationships:
            pass

        # process endorsementDetails
        my_endorsement = EndorsementDetails(fk_object_id=self.id,
                                            foreignKeyObjectType='dataset',
                                            endorsement=self.endorsementDetails['endorsement'],
                                            certifiedBy=self.endorsementDetails['certifiedBy'])

        # process expressions
        for expression in self.expressions:
            my_expression = Expression(name=expression['name'], 
                                          fk_dataset_id=self.id, 
                                          description=expression['description'], 
                                          expression=expression['expression'])

        # process roles
        for role in self.roles:
            my_role = Role(name=role['name'], 
                           modelPermission=role['modelPermission'], 
                           fk_dataset_id=self.id)

        # process uptreamDataflows
        for uptreamDataflow in self.uptreamDataflows:
            my_upstreamDataflow = UpstreamDataflow(targetDataflowId=uptreamDataflow['targetDataflowId'],
                                                    groupId=uptreamDataflow['groupId'],
                                                    fk_object_id=self.id,
                                                    foreignKeyObjectType='dataset')

        # process datasourceUsages
        for datasourceUsage in self.datasourceUsages:
            my_datasourceUsage = DatasourceUsage(datasourceInstanceId=datasourceUsage['datasourceInstanceId'],
                                                fk_object_id=self.id,
                                                foreignKeyObjectType='dataset')

        # process sensitivityLabel
        for sensitivityLabel in self.sensitivityLabel:
            my_sensitivityLabel = SensitivityLabel(labelId=sensitivityLabel['labelId'],
                                                  fk_object_id=self.id,
                                                  foreignKeyObjectType='dataset')

        # process users
        for user in self.users:
            my_user = User(displayName=user['displayName'],
                           fk_object_id=self.id,
                           foreignKeyObjectType='dataset',
                           emailAddress=user['emailAddress'],
                           appUserAccessRight=user['appUserAccessRight'],
                           identifier=user['identifier'],
                           graphId=user['graphId'],
                           principalType=user['principalType'],
                           userType=user['userType'],
                           profile=user['profile'])



class Datamart_user:
    """
    This class will be used to create the datamart_users table
    """
    def __init__(self, displayName:str, fk_datamart_id:str, email_address:str, identifier:str, 
                 graphId:str, principalType:str, userType:str, profile:dict, datamartUserAccessRight:str):
        self.displayName = displayName
        self.fk_datamart_id = fk_datamart_id
        self.email_address = email_address
        self.identifier = identifier
        self.graphId = graphId
        self.principalType = principalType
        self.userType = userType
        self.profile = profile
        self.datamartUserAccessRight = datamartUserAccessRight


class Column:
    """
    This class will be used to create the column table
    """
    def __init__(self, name:str, dataType:str, isHidden:bool, fk_dataset_id:str, table_name:str):
        self.name = name
        self.dataType = dataType
        self.isHidden = isHidden
        self.fk_dataset_id = fk_dataset_id
        self.table_name = table_name

class Measure:
    """
    This class will be used to create the measure table
    """
    def __init__(self, name:str, expression:str, fk_dataset_id:str, table_name:str):
        self.name = name
        self.expression = expression
        self.fk_dataset_id = fk_dataset_id
        self.table_name = table_name

class Source:
    """
    This class will be used to create the source table
    """
    def __init__(self, expression:str, fk_dataset_id:str, table_name:str):
        self.expression = expression
        self.fk_dataset_id = fk_dataset_id
        self.table_name = table_name


class Member:
    """
    This class will be used to create the member table
    """
    def __init__(self, role_name:str, fk_dataset_id:str, memberName:str, memberId:str, memberType:str, identityProvider:str):
        self.role_name = role_name
        self.fk_dataset_id = fk_dataset_id
        self.memberName = memberName
        self.memberId = memberId
        self.memberType = memberType
        self.identityProvider = identityProvider

class TablePermission:
    """
    This class will be used to create the table_permission table
    """
    def __init__(self, role_name:str, fk_dataset_id:str, name:str, filterExpression:str):
        self.role_name = role_name
        self.fk_dataset_id = fk_dataset_id
        self.name = name
        self.filterExpression = filterExpression

