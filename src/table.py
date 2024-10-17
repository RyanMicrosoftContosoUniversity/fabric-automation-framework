"""
This module will be used for table objects within the metadata database
This will take results from the scan and create tables in the metadata database
"""
from src.table_writer import TableWriter, FileWriter

class EndorsementDetails:
    """
    This class will be used to create the endorsementDetails table
    """
    def __init__(self, fk_object_id:str, foreignKeyObjectType:str, endorsement:str, certifiedBy:str):
        self.fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType
        self.endorsement = endorsement
        self.certifiedBy = certifiedBy

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['report', 'dataflow', 'datamart', 'dataset']:
            raise ValueError('foreignKeyObjectType must be one of the following: report, dataflow, datamart, dataset')

class Tile:
    """
    This class will be used to create the tile table
    """
    def __init__(self, id:str, title:str, report_id:str, dataset_id:str, fk_dashboard_id:str):
        self.id = id
        self.title = title
        self.report_id = report_id
        self.dataset_id = dataset_id
        self.fk_dashboard_id = fk_dashboard_id   
class Table:
    """
    This class will be used to create the table table
    """
    def __init__(self, name:str, fk_dataset_id:str, column:list=[], measure:list=[], source:list=[]):
        self.name = name
        self.fk_dataset_id = fk_dataset_id
        self.column = column
        self.measure = measure
        self.source = source

        # process column
        for column in self.column:
            my_column = Column(name=column['name'], dataType=column['dataType'], isHidden=column['isHidden'], fk_dataset_id=self.fk_dataset_id, table_name=self.name)

            # write to file
            my_column_line = f'{my_column.name},{my_column.dataType},{my_column.isHidden},{my_column.fk_dataset_id},{my_column.table_name}\n'
            column_file_writer = FileWriter(file_type='column')
            if column_file_writer.line_exists(my_column_line):
                pass
            else:
                column_file_writer.append_line_to_file(my_column_line)

        # process measure
        for measure in self.measure:
            my_measure = Measure(name=measure['name'], expression=measure['expression'], fk_dataset_id=self.fk_dataset_id, table_name=self.name)

            # write to file
            my_measure_line = f'{my_measure.name},{my_measure.expression},{my_measure.fk_dataset_id},{my_measure.table_name}\n'
            measure_file_writer = FileWriter(file_type='measure')
            if measure_file_writer.line_exists(my_measure_line):
                pass
            else:
                measure_file_writer.append_line_to_file(my_measure_line)

        # process source
        for source in self.source:
            my_source = Source(expression=source['expression'], fk_dataset_id=self.fk_dataset_id, table_name=self.name)

            # write to file
            my_source_line = f'{my_source.expression},{my_source.fk_dataset_id},{my_source.table_name}\n'
            source_file_writer = FileWriter(file_type='source')
            if source_file_writer.line_exists(my_source_line):
                pass
            else:
                source_file_writer.append_line_to_file(my_source_line)




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
    def __init__(self, name:str, modelPermission:str, fk_dataset_id:str, member:list=[], tablePermission:list=[]):
        self.name = name
        self.modelPermission = modelPermission
        self.fk_dataset_id = fk_dataset_id
        self.member = member
        self.tablePermission = tablePermission

        # process member
        for member in self.member:
            my_member = Member(role_name=self.name, fk_dataset_id=self.fk_dataset_id, memberName=member['memberName'], memberId=member['memberId'], memberType=member['memberType'], identityProvider=member['identityProvider'])

            # write to file
            my_member_line = f'{my_member.role_name},{my_member.fk_dataset_id},{my_member.memberName},{my_member.memberId},{my_member.memberType},{my_member.identityProvider}\n'
            member_file_writer = FileWriter(file_type='member')
            if member_file_writer.line_exists(my_member_line):
                pass
            else:
                member_file_writer.append_line_to_file(my_member_line)

        # process tablePermission
        for tablePermission in self.tablePermission:
            my_tablePermission = TablePermission(role_name=self.name, fk_dataset_id=self.fk_dataset_id, name=tablePermission['name'], filterExpression=tablePermission['filterExpression'])

            # write to file
            my_tablePermission_line = f'{my_tablePermission.role_name},{my_tablePermission.fk_dataset_id},{my_tablePermission.name},{my_tablePermission.filterExpression}\n'
            tablePermission_file_writer = FileWriter(file_type='tablePermission')
            if tablePermission_file_writer.line_exists(my_tablePermission_line):
                pass
            else:
                tablePermission_file_writer.append_line_to_file(my_tablePermission_line)

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
        self.fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['report', 'dataflow', 'datamart', 'dataset', 'dashboard']:
            raise ValueError('foreignKeyObjectType must be one of the following: report, dataflow, datamart, dataset, dashboard')

class User:
    """
    This class will be used to create the user table
    """
    def __init__(self, displayName:str, fk_object_id:str, foreignKeyObjectType:str, 
                 emailAddress:str, appUserAccessRight:str, identifier:str, 
                 graphId:str, principalType:str, userType:str, profile:dict):
        self.displayName = displayName
        self.fk_object_id = fk_object_id
        self.foreignKeyObjectType = foreignKeyObjectType
        self.emailAddress = emailAddress
        self.appUserAccessRight = appUserAccessRight
        self.identifier = identifier
        self.graphId = graphId
        self.principalType = principalType
        self.userType = userType
        self.profile = profile

        # validate foreignKeyObjectType
        if self.foreignKeyObjectType not in ['workspace', 'report', 'dataflow', 'dataset', 'dashboard']:
            raise ValueError('foreignKeyObjectType must be one of the following: workspace, report, dataflow, dataset, dashboard')


class Workspace_table:
    """
    This class will be used to create the workspace table
    """
    def __init__(self, id:str, name:str, type:str, isOnDedicatedCapacity:bool,  
                 defaultDatasetStorageFormat:str=None, capacityId:str=None, reports:list=None,
                   dashboards:list=None, dataflows:list=None,
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
            try:
                endorsementDetails = report['endorsementDetails']
            except:
                endorsementDetails = {}
            try:
                sensitivityLabel = report['sensitivityLabel']
            except:
                sensitivityLabel = {}
            try:
                users = report['users']
            except:
                users = []
            report_table = Report_table(id=report['id'], workspaceId=self.id, name=report['name'],
                                        datasetId=report['datasetId'], createdDateTime=report['createdDateTime'],
                                        modifiedDateTime=report['modifiedDateTime'], modifiedBy=report['modifiedBy'],
                                        endorsementDetails=endorsementDetails, sensitivityLabel=sensitivityLabel,
                                        users=users, )

        # process dashboards
        for dashboard in self.dashboards:
            dashboard_table = Dashboard_table(id=dashboard['id'], workspaceId=self.id, isReadOnly=dashboard['isReadOnly'],
                                              tiles=dashboard['tiles'], sensitivityLabel=dashboard['sensitivityLabel'],
                                              users=dashboard['users'])

        # process dataflows
        for dataflow in self.dataflows:
            try:
                description = dataflow['description']
            except:
                description = None
            try:
                endorsementDetails = dataflow['endorsementDetails']
            except:
                endorsementDetails = {}
            try:
                datasourceUsages = dataflow['datasourceUsages']
            except:
                datasourceUsages = []
            try:
                misconfiguredDatasourceUsages = dataflow['misconfiguredDatasourceUsages']
            except:
                misconfiguredDatasourceUsages = []
            try:
                sensitivityLabel = dataflow['sensitivityLabel']
            except:
                sensitivityLabel = {}
            try:
                users = dataflow['users']
            except:
                users = []  
            dataflow_table = Dataflow_table(objectId=dataflow['objectId'], workspaceId=self.id, name=dataflow['name'],
                                            description=description, configuredBy=dataflow['configuredBy'], modifiedBy=dataflow['modifiedBy'],
                                            modifiedDateTime=dataflow['modifiedDateTime'], endorsementDetails=endorsementDetails,
                                            datasourceUsages=datasourceUsages, misconfiguredDatasourceUsages=misconfiguredDatasourceUsages,
                                            sensitivityLabel=sensitivityLabel, users=users)    

        # process datamarts
        for datamart in self.datamarts:
            datamart_table = Datamart_table(id=datamart['id'], workspaceId=self.id, name=datamart['name'],
                                            description=datamart['description'], type=datamart['type'], configuredBy=datamart['configuredBy'],
                                            configuredById=datamart['configuredById'], modifiedBy=datamart['modifiedBy'], modifiedDateTime=datamart['modifiedDateTime'],
                                            sensitivityLabel=datamart['sensitivityLabel'], endorsementDetails=datamart['endorsementDetails'],
                                            upstreamDataflows=datamart['UpstreamDataflows'], datasourceUsages=datamart['datasourceUsages'], users=datamart['Users'])

        # process datasets
        for dataset in self.datasets:
            try:
                relationships = dataset['relationships']
            except:
                relationships = []
            try:
                endorsementDetails = dataset['endorsementDetails']
            except:
                endorsementDetails = {}
            try:
                expressions = dataset['expressions']
            except:
                expressions = []
            try:
                roles = dataset['roles']
            except:
                roles = []
            try:
                upstreamDataflows = dataset['upstreamDataflows']
            except:
                upstreamDataflows = []
            try:
                DatasourceUsages = dataset['datasourceUsages']
            except:
                DatasourceUsages = []
            try:
                SensitivityLabel = dataset['sensitivityLabel']
            except:
                SensitivityLabel = []
            try:
                users = dataset['users']
            except:
                users = []
            dataset_table = Dataset_table(id=dataset['id'], name=dataset['name'], workspaceId=self.id, tables=dataset['tables'], relationships=relationships,
                                          configuredBy=dataset['configuredBy'], endorsementDetails=endorsementDetails, expressions=expressions,
                                          roles=roles, uptreamDataflows=upstreamDataflows, datasourceUsages=DatasourceUsages,
                                          sensitivityLabel=SensitivityLabel, users=users)
            
        # process users
        if self.users!=None:
            for user in self.users:
                workspace_users_table = Workspace_users_table(displayName=user['displayName'], workspaceId=self.id, emailAddress=user['emailAddress'],
                                                            appUserAccessRight=user['appUserAccessRight'], identifier=user['identifier'], graphId=user['graphId'],
                                                            principalType=user['principalType'])


        # write workspace to file
        workspace_line = f'{self.id},{self.name},{self.type},{self.isOnDedicatedCapacity},{self.capacityId},{self.defaultDatasetStorageFormat}\n'
        workspace_file_writer = FileWriter(file_type='workspace')
        if workspace_file_writer.line_exists(workspace_line):
            pass
        else:
            workspace_file_writer.append_line_to_file(workspace_line)

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

        # process tiles
        for tile in self.tiles:
            my_tile = Tile(id=tile['id'], title=tile['title'], report_id=tile['reportId'], dataset_id=tile['datasetId'], fk_dashboard_id=self.id)

            # write to file
            my_tile_line = f'{my_tile.id},{my_tile.title},{my_tile.report_id},{my_tile.dataset_id},{my_tile.fk_dashboard_id}\n'
            tile_file_writer = FileWriter(file_type='tile')
            if tile_file_writer.line_exists(my_tile_line):
                pass
            else:
                tile_file_writer.append_line_to_file(my_tile_line)

        # process sensitivityLabel
        my_sensitivityLabel = SensitivityLabel(labelId=sensitivityLabel['labelId'],
                                            fk_object_id=self.id,
                                            foreignKeyObjectType='dashboard')
        
        # write to file
        my_sensitivityLabel_line = f'{my_sensitivityLabel.labelId},{my_sensitivityLabel.fk_object_id},{my_sensitivityLabel.foreignKeyObjectType}\n'
        sensitivityLabel_file_writer = FileWriter(file_type='sensitivityLabel')
        if sensitivityLabel_file_writer.line_exists(my_sensitivityLabel_line):
            pass
        else:
            sensitivityLabel_file_writer.append_line_to_file(my_sensitivityLabel_line)

        # process users
        for user in self.users:
            try:
                user_type = user['userType']
            except:
                user_type = 'None'
            try:
                profile = user['profile']
            except:
                profile = 'None'
            my_user = User(displayName=user['displayName'],
                           fk_object_id=self.id,
                           foreignKeyObjectType='dashboard',
                           emailAddress=user['emailAddress'],
                           appUserAccessRight=user['appUserAccessRight'],
                           identifier=user['identifier'],
                           graphId=user['graphId'],
                           principalType=user['principalType'],
                           userType=user_type,
                           profile=profile
                           )
            
            # write to file
            my_user_line = f'{my_user.displayName},{my_user.fk_object_id},{my_user.foreignKeyObjectType},{my_user.emailAddress},{my_user.appUserAccessRight},{my_user.identifier},{my_user.graphId},{my_user.principalType},{my_user.userType},{my_user.profile}\n'
            user_file_writer = FileWriter(file_type='user')
            if user_file_writer.line_exists(my_user_line):
                pass
            else:
                user_file_writer.append_line_to_file(my_user_line)

        # write dashboard to file
        dashboard_line = f'{self.id},{self.workspaceId},{self.isReadOnly}\n'
        dashboard_file_writer = FileWriter(file_type='dashboard')
        if dashboard_file_writer.line_exists(dashboard_line):
            pass
        else:
            dashboard_file_writer.append_line_to_file(dashboard_line)
        
            



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
    def __init__(self, id:str, name:str, workspaceId:str, tables:list,
                 configuredBy:str, endorsementDetails:dict={}, relationships:list=[], expressions:list=[], roles:list=[],
                 uptreamDataflows:list=[], datasourceUsages:list=[], sensitivityLabel:dict=[], users:list=[]):
        self.id = id
        self.name = name
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
            my_table = Table(name=table['name'], fk_dataset_id=self.id, column=table['columns'], 
                             measure=table['measures'], source=table['source'])

            # write to file
            my_table_line = f'{my_table.name},{my_table.fk_dataset_id}\n'
            table__file_writer = FileWriter(file_type='table')
            if table__file_writer.line_exists(my_table_line):
                pass
            else:
                table__file_writer.append_line_to_file(my_table_line)

        # process relationships
        for relationship in self.relationships:
            pass

        # process endorsementDetails
        try:
            endorsement = self.endorsementDetails['endorsement']
        except:
            endorsement = 'None'
        try:
            certifiedBy = self.endorsementDetails['certifiedBy']
        except:
            certifiedBy = 'None'
        my_endorsement = EndorsementDetails(fk_object_id=self.id,
                                            foreignKeyObjectType='dataset',
                                            endorsement=endorsement,
                                            certifiedBy=certifiedBy)
        # write to file
        my_endorsement_line = f'{my_endorsement.fk_object_id},{my_endorsement.foreignKeyObjectType},{my_endorsement.endorsement},{my_endorsement.certifiedBy}\n'

        endorsement_file_writer = FileWriter(file_type='endorsementDetail')
        if endorsement_file_writer.line_exists(my_endorsement_line):
            pass
        else:
            endorsement_file_writer.append_line_to_file(my_endorsement_line)

        # process expressions
        for expression in self.expressions:
            my_expression = Expression(name=expression['name'], 
                                          fk_dataset_id=self.id, 
                                          description=expression['description'], 
                                          expression=expression['expression'])
            
            # write to file
            my_expression_line = f'{my_expression.name},{my_expression.fk_dataset_id},{my_expression.description},"""{my_expression.expression}"""\n'
            expression_file_writer = FileWriter(file_type='expression')
            if expression_file_writer.line_exists(my_expression_line):
                pass
            else:
                expression_file_writer.append_line_to_file(my_expression_line)

        # process roles
        for role in self.roles:
            my_role = Role(name=role['name'], 
                           modelPermission=role['modelPermission'], 
                           fk_dataset_id=self.id,
                           member=role['members'],
                           tablePermission=role['tablePermissions'])
            
            # write to file
            my_role_line = f'{my_role.name},{my_role.modelPermission},{my_role.fk_dataset_id}\n'
            role_file_writer = FileWriter(file_type='role')
            if role_file_writer.line_exists(my_role_line):
                pass
            else:
                role_file_writer.append_line_to_file(my_role_line)

        # process uptreamDataflows
        for uptreamDataflow in self.uptreamDataflows:
            my_upstreamDataflow = UpstreamDataflow(targetDataflowId=uptreamDataflow['targetDataflowId'],
                                                    groupId=uptreamDataflow['groupId'],
                                                    fk_object_id=self.id,
                                                    foreignKeyObjectType='dataset')
            
            # write to file
            my_upstreamDataflow_line = f'{my_upstreamDataflow.targetDataflowId},{my_upstreamDataflow.groupId},{my_upstreamDataflow.fk_object_id},{my_upstreamDataflow.foreignKeyObjectType}\n'
            upstreamDataflow_file_writer = FileWriter(file_type='upstreamDataflow')
            if upstreamDataflow_file_writer.line_exists(my_upstreamDataflow_line):
                pass
            else:
                upstreamDataflow_file_writer.append_line_to_file(my_upstreamDataflow_line)


        # process datasourceUsages
        for datasourceUsage in self.datasourceUsages:
            my_datasourceUsage = DatasourceUsage(datasourceInstanceId=datasourceUsage['datasourceInstanceId'],
                                                fk_object_id=self.id,
                                                foreignKeyObjectType='dataset')
            
            # write to file
            my_datasourceUsage_line = f'{my_datasourceUsage.datasourceInstanceId},{my_datasourceUsage.fk_object_id},{my_datasourceUsage.foreignKeyObjectType}\n'
            datasourceUsage_file_writer = FileWriter(file_type='datasourceUsage')
            if datasourceUsage_file_writer.line_exists(my_datasourceUsage_line):
                pass
            else:
                datasourceUsage_file_writer.append_line_to_file(my_datasourceUsage_line)


        # process sensitivityLabel
        if len(sensitivityLabel) == 0:
            sensitivityLabel = [{'labelId': 'None'}]
        else:
            my_sensitivityLabel = SensitivityLabel(labelId=sensitivityLabel['labelId'],
                                                    fk_object_id=self.id,
                                                    foreignKeyObjectType='dataset')
                
            # write to file
            my_sensitivityLabel_line = f'{my_sensitivityLabel.labelId},{my_sensitivityLabel.fk_object_id},{my_sensitivityLabel.foreignKeyObjectType}\n'
            sensitivityLabel_file_writer = FileWriter(file_type='sensitivityLabel')
            if sensitivityLabel_file_writer.line_exists(my_sensitivityLabel_line):
                pass
            else:
                sensitivityLabel_file_writer.append_line_to_file(my_sensitivityLabel_line)


        # process users
        for user in self.users:
            try:
                user_type = user['userType']
            except:
                user_type = 'None'
            try:
                profile = user['profile']
            except:
                profile = 'None'
            my_user = User(displayName=user['displayName'],
                           fk_object_id=self.id,
                           foreignKeyObjectType='dataset',
                           emailAddress=user['emailAddress'],
                           appUserAccessRight=user['appUserAccessRight'],
                           identifier=user['identifier'],
                           graphId=user['graphId'],
                           principalType=user['principalType'],
                           userType=user_type,
                           profile=profile
                           )
            
            # write to file
            my_user_line = f'{my_user.displayName},{my_user.fk_object_id},{my_user.foreignKeyObjectType},{my_user.emailAddress},{my_user.appUserAccessRight},{my_user.identifier},{my_user.graphId},{my_user.principalType},{my_user.userType},{my_user.profile}\n'
            user_file_writer = FileWriter(file_type='user')
            if user_file_writer.line_exists(my_user_line):
                pass
            else:
                user_file_writer.append_line_to_file(my_user_line)

        # write dataset to file
        dataset_line = f'{self.id},{self.name},{self.workspaceId}\n'
        dataset_file_writer = FileWriter(file_type='dataset')
        if dataset_file_writer.line_exists(dataset_line):
            pass
        else:
            dataset_file_writer.append_line_to_file(dataset_line)




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



