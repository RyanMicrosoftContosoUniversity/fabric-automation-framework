from __future__ import annotations
import requests
from typing import List, Dict, Any, Optional
import uuid




class DecisionRules:
    """
    create a DecisionRules object to hold the following attributes

    effect:str: Permit (only value allowed)
    permission:list[dict]:
    constraints:dict{columns:list, rows:list}
    """
    def __init__(
        self, 
        effect:str, 
        permission:list[dict[str, Any]], 
        constraints:dict[str, Any]
    ):
        # validate effect
        if effect != 'Permit':
            raise ValueError('Effect must be Permit')
        
        self.effect = effect
        self.permissions_list = permission
        self.constraints_dict = constraints

        self.definition = [
            {
                'effect': self.effect,
                'permission': self.permissions_list,
                'constraints': self.constraints_dict,
            }
        ]

class DecisionRuleNew(list[dict]):
    """
    create a DecisionRule with Effect, Permission, and Constraints attributes.
    
    args:
        effect:str: The effect of the decision rule (only 'Permit' is allowed)
        permission:PermissionRule: The list of permission attribute dictionaries
        constraints:Constraints: The constraints dictionary containing column and row constraints

    Example:
        >>> decision_rule = DecisionRuleNew(
        ...     effect='Permit',
        ...     permission=PermissionRule(path='doctor_table'),
        ...     constraints=Constraints(columns=[], rows=[])
        ... )
        >>> print(decision_rule)
        [
            {
                'effect': 'Permit',
                'permission': [{'attributeName': 'Path', 'attributeValueIncludedIn': ['/Tables/doctor_table']}],
                'constraints': {'columns': [], 'rows': []}
            }
        ]
        
    Raises:
        ValueError: If effect is not 'Permit'
    """
    def __init__(
        self, 
        effect:str, 
        permission:PermissionRule, 
        constraints:Constraints
    ):
        # validate effect
        if effect != 'Permit':
            raise ValueError('Effect must be Permit')
        
        super().__init__()  # Initialize the list

        self.append({
            'effect': effect,
            'permission': permission,
            'constraints': constraints,
        })
        

class Members:
    """
    create members to be added to a data access role in OneLake

    fabricItemMembers:list[dict]
    """
    def __init__(self, fabricItemMembers:list[dict], msEntraMembers:list[dict]=[]):
        self.fabricItemMembers = fabricItemMembers

        if msEntraMembers:
            self.microsoftEntraMembers = msEntraMembers
        else:
            self.microsoftEntraMembers=[]

        self.definition = {
    'microsoftEntraMembers': self.microsoftEntraMembers,
    'fabricItemMembers': self.fabricItemMembers
}
        
class PermissionRule(list[dict]):
    def __init__(self, path: str):
        """Create a PermissionRule with Path and Action attributes.
        
        Args:
            path (str): Table name (e.g., 'doctor_table') or 'all' for all tables.
                Will be automatically formatted to '/Tables/table_name' or '/Tables/*' for 'all'.
        
        Returns:
            PermissionRule: A list containing Path and Action attribute dictionaries
        
        Example:
            >>> perm_rule = PermissionRule(path='doctor_table')
            >>> print(perm_rule)
            [
                {
                  "attributeName": "Path",
                  "attributeValueIncludedIn": [
                    "/Tables/doctor_table"
                  ]
                },
                {
                  "attributeName": "Action",
                  "attributeValueIncludedIn": [
                    "Read"
                  ]
                }
            ]
            
        Raises:
            ValueError: If path is not a string or is empty
        """
        super().__init__()  # Initialize the list
        
        # Validate the path
        self._validate_path(path)
        
        # Convert path to proper format
        formatted_path = self._format_path(path)
        
        # Create the Path attribute
        path_attribute = {
            "attributeName": "Path",
            "attributeValueIncludedIn": [formatted_path]
        }
        
        # Create the Action attribute (always Read)
        action_attribute = {
            "attributeName": "Action", 
            "attributeValueIncludedIn": ["Read"]
        }
        
        # Add both attributes to the list
        self.append(path_attribute)
        self.append(action_attribute)

    def _validate_path(self, path: str):
        """
        Validate the path parameter
        """
        if not isinstance(path, str):
            raise ValueError(f'path must be a string, got: {type(path).__name__}')
        if not path.strip():
            raise ValueError('path cannot be empty')

    def _format_path(self, path: str):
        """
        Convert path to proper format
        """
        path = path.strip()
        if path.lower() == 'all':
            return '/Tables/*'
        else:
            # Remove any existing /Tables/ prefix if present
            if path.startswith('/Tables/'):
                path = path[8:]  # Remove '/Tables/'
            return f'/Tables/{path}'

    def add(self, path: str):
        """Add an additional table path to the existing Path attribute.
        
        Args:
            path (str): Table name to add (e.g., 'memo_table'). Will be automatically
                formatted to '/Tables/table_name'. Use 'all' for wildcard '/Tables/*'.
                
        Raises:
            ValueError: If path is not a string or is empty
            RuntimeError: If Path attribute is not found in PermissionRule
            
        Example:
            >>> perm_rule = PermissionRule(path='doctor_table')
            >>> perm_rule.add('memo_table')
            >>> perm_rule[0]['attributeValueIncludedIn']
            ['/Tables/doctor_table', '/Tables/memo_table']
        """
        # Validate the path
        self._validate_path(path)
        
        # Format the path
        formatted_path = self._format_path(path)
        
        # Find the Path attribute (should be the first element)
        path_attribute = None
        for attr in self:
            if attr.get("attributeName") == "Path":
                path_attribute = attr
                break
        
        if path_attribute is None:
            raise RuntimeError("Path attribute not found in PermissionRule")
        
        # Add the new path if it doesn't already exist
        if formatted_path not in path_attribute["attributeValueIncludedIn"]:
            path_attribute["attributeValueIncludedIn"].append(formatted_path)

class RowConstraint(list[dict]):
    def __init__(self, table: str, rls_definition: str):
        """Create a row-level security constraint for OneLake data access roles.
        
        Args:
            table (str): The table name or path. If it doesn't start with '/Tables/', 
                the prefix will be automatically added (e.g., 'doctor_table' becomes '/Tables/doctor_table')
            rls_definition (str): The SQL query to apply for row-level security. 
                Must start with 'SELECT * FROM' (e.g., 'SELECT * FROM doctor_table WHERE department = "Gastroenterology"')
        
        Returns:
            RowConstraint: A list containing row constraint dictionaries
            
        Example:
            >>> constraint = RowConstraint(
            ...     table="doctor_table",
            ...     rls_definition="SELECT * FROM doctor_table WHERE department = 'Gastroenterology'"
            ... )
            >>> print(constraint)
            [
              {
                "tablePath": "/Tables/doctor_table",
                "value": "SELECT * FROM doctor_table WHERE department = 'Gastroenterology'"
              }
            ]
            
        Raises:
            ValueError: If table is not a string, is empty, or rls_definition doesn't start with 'SELECT * FROM'
        """
        super().__init__()  # Initialize the list

        # Validate and format the table path
        table_path = self._validate_and_format_table(table)
        
        # Validate RLS definition
        self._validate_rls_definition(rls_definition)
        
        # Store the formatted table path as an attribute
        self.table = table_path
        self.rls_definition = rls_definition
        
        # Add the first constraint to the list
        self.append({
            'tablePath': table_path,
            'value': rls_definition
        })

    def _validate_and_format_table(self, table: str) -> str:
        """
        Validate and format the table parameter to include /Tables/ prefix if needed
        """
        if not isinstance(table, str):
            raise ValueError(f'table must be a string, got: {type(table).__name__}')
        
        if not table.strip():
            raise ValueError('table cannot be empty')
            
        table = table.strip()
        
        # Add /Tables/ prefix if not present
        if not table.startswith('/Tables/'):
            table = f'/Tables/{table.lstrip("/")}'
            
        return table

    def _validate_rls_definition(self, rls_definition: str):
        """
        Validate the RLS definition parameter
        """
        if not isinstance(rls_definition, str):
            raise ValueError(f'rls_definition must be a string, got: {type(rls_definition).__name__}')
            
        if not rls_definition.strip():
            raise ValueError('rls_definition cannot be empty')
            
        # validate rls_definition starts with SELECT * FROM
        if not rls_definition.strip().upper().startswith('SELECT * FROM'):
            raise ValueError(f'rls_definition must start with SELECT * FROM, got: {rls_definition}')

    def _validate_constraint(self, table_path: str, rls_definition: str):
        """
        Validate a single constraint's attributes (for backward compatibility)
        """
        formatted_table = self._validate_and_format_table(table_path)
        self._validate_rls_definition(rls_definition)
        return formatted_table, rls_definition

    def add_constraint(self, table: str, rls_definition: str):
        """Add another row constraint to the RowConstraint list.
        
        Args:
            table (str): The table name or path. If it doesn't start with '/Tables/', 
                the prefix will be automatically added (e.g., 'nurse_table' becomes '/Tables/nurse_table')
            rls_definition (str): The SQL query for the additional row-level security rule.
                Must start with 'SELECT * FROM' (e.g., 'SELECT * FROM nurse_table WHERE shift = "day"')
        
        Raises:
            ValueError: If table is invalid or rls_definition doesn't start with 'SELECT * FROM'
            
        Example:
            >>> constraint = RowConstraint("doctor_table", "SELECT * FROM doctor_table WHERE department = 'Cardiology'")
            >>> constraint.add_constraint("nurse_table", "SELECT * FROM nurse_table WHERE shift = 'day'")
            >>> len(constraint)
            2
        """
        # Validate and format the new constraint
        formatted_table = self._validate_and_format_table(table)
        self._validate_rls_definition(rls_definition)

        # append to RowConstraint Object list
        self.append({
            'tablePath': formatted_table,
            'value': rls_definition
        })
        

class ColumnConstraint(list[dict]):
    def __init__(self, table:str, column_names:list[str], column_effect:str, column_action:list[str]):
        """
        args:
            table:str: The relative path the column constraint will be applied to
            column_names:list[str]: The list of column names to apply the constraint to
            column_effect:str: The effect of the column constraint (e.g., "mask", "redact")
            column_action:list[str]: The actions to apply to the column (only READ is available)

            Example:
            [
              {
                "tablePath": "/Tables/doctor_table",
                "columnNames": [
                  "*"
                ],
                "columnEffect": "Permit",
                "columnAction": [
                  "Read"
                ]
              }
            ]
        """
        super().__init__()  # Initialize the list

        table_path = table
        table_path, column_names, column_effect, column_action = self._validate_constraint(table_path, column_names, column_effect, column_action)

        self.append({
            'tablePath': table_path,
            'columnNames': column_names,
            'columnEffect': column_effect,
            'columnAction': column_action
        })

    def _validate_constraint(self, table_path:str, column_names:list[str], column_effect:str, column_action:list[str]):
        """
        Validate a single constraint's attributes
        """
        if not isinstance(table_path, str):
            raise ValueError(f'table_path must be a string got: {table_path}')
        if not isinstance(column_names, list):
            raise ValueError(f'column_names must be a list got: {column_names}')
        # if table_path does not start with /Tables/, prefix it
        if not table_path.startswith('/Tables/'):
            table_path = f'/Tables/{table_path.lstrip("/")}'
        for name in column_names:
            if not isinstance(name, str):
                raise ValueError(f'column_names must be a list of strings got: {name}')
        if not isinstance(column_effect, str):
            raise ValueError(f'column_effect must be a string got: {column_effect}')
        if not isinstance(column_action, list):
            raise ValueError(f'column_action must be a list got: {column_action}')
        for action in column_action:
            if not isinstance(action, str):
                raise ValueError(f'column_action must be a list of strings got: {action}')
            if action != 'Read':
                raise ValueError(f'column_action must be Read got: {action}')
        
        return table_path, column_names, column_effect, column_action

    def add_constraint(self, table_path:str, column_names:list[str], column_effect:str, column_action:list[str]):
        """
        Add a column constraint to the ColumnConstraint list
        """
        # validate the new constraint
        self._validate_constraint(table_path, column_names, column_effect, column_action)

        # append to ColumnConstraint Object list
        self.append({
            'tablePath': table_path,
            'columnNames': column_names,
            'columnEffect': column_effect,
            'columnAction': column_action
        })

class Constraints(dict):
    def __init__(self, columns:ColumnConstraint, rows:RowConstraint):
        """
        args:
            columns:ColumnConstraint
            rows:RowConstraint
        """
        self.definition = {
            'columns': columns,
            'rows': rows
        }

class DataAccessRole:
    def __init__(self, decisionRules:DecisionRules, id:str, members:Members, name:str):
        """
        args:decisionRules:DecisionRule[], id:str, members:Members, name:str
        """
        self.decisionRulesDefinition = decisionRules.definition
        self.membersDefinition = members.definition
        role = {
                'name': name,
                'decisionRules': self.decisionRulesDefinition,
                'members': self.membersDefinition
                }
        if id:
            role['id'] = id
        self.definition = {'value': [role]}

    
    @staticmethod
    def create_update_data_access_role(workspace_id:str, item_id:str, data_access_role:DataAccessRole, api_token:str):
        """
        Create or update a data access role in OneLake
        PUT https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/dataAccessRoles
        https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-data-access-security/create-or-update-data-access-roles?tabs=HTTP#create-or-update-data-access-roles-example

        args:
            workspace_id:str: The guid of the workspace where the lakehouse resides
            item_id:str: The guid of the lakehouse to create the role in
            token:str: The API token for authentication

        """
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/dataAccessRoles'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, json=data_access_role.definition)

        return response
    

    @staticmethod
    def upsert_data_access_role(workspace_id:str, item_id:str, role:DataAccessRole, api_token:str):
        """
        """
        base = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/dataAccessRoles'
        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        # read existing
        existing = requests.get(base, headers=headers).json().get('value', [])

        new_role = role.definition['value'][0]
        # if id not set, try match by name; else assign a new id

        match = None
        if 'id' in new_role:
            match = next((r for r in existing if r.get('id')==new_role['id']), None)
        if not match:
            match = next((r for r in existing if r.get('name', '').lower()==new_role['name'].lower()), None)

        if match:
            # update in place
            match.update({k:v for k,v in new_role.items() if k!='id' or new_role.get('id')})
        else:
            new_role.setdefault('id', str(uuid.uuid4()))
            existing.append(new_role)
        
        # 2 write back full set
        return requests.put(base, headers=headers, json={'value':existing})

    @staticmethod
    def list_data_access_roles(workspace_id:str, item_id:str, api_token:str):
        """
        GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{itemId}/dataAccessRoles
        https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-data-access-security/list-data-access-roles?tabs=HTTP
        """
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/dataAccessRoles'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        return response

