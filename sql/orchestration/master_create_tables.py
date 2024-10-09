"""
Orchestration script to create tables in correct order
"""
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc

# get sql admin credentials
key_vault_name = 'kvfabricnonprodeus2rh'
secret_name = 'sql-admin-credentials'

# Construct the Key Vault URL
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a SecretClient
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Retrieve the secret
retrieved_secret = client.get_secret(secret_name)

# Print the secret value
print(f'The value of the secret "{secret_name}" is: {retrieved_secret.value}')

# define connection string
conn_str = (
    f'DRIVER={"ODBC Driver 17 for SQL Server"};'
    f'SERVER=:tcp:fabric-metadata-server.database.windows.net,1433'
    f'DATABASE=fabric-metadata-db;'
    f'UID=rharrington;'
    f'PWD={retrieved_secret.value}'
    f'Encrypt=yes;'
    f'TrustServerCertificate=no;'
    f'Connection Timeout=60;'
)

conn_str_2 = f'Driver={"ODBC Driver 17 for SQL Server"};Server=tcp:fabric-metadata-server.database.windows.net,1433;Database=fabric-metadata-db;Uid=rharrington;Pwd={retrieved_secret.value};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'
# establish the connection
conn = pyodbc.connect(conn_str_2)
cursor = conn.cursor()

# correct order for table creation
sql_create_list = [
    r'sql\create_tables\create_table_workspace.sql',
    r'sql\create_tables\create_dateset.sql',
    r'sql\create_tables\create_table_user.sql',
    r'sql\create_tables\create_table_expression.sql',
    r'sql\create_tables\create_table_table.sql',
    r'sql\create_tables\create_table_role.sql',
    r'sql\create_tables\create_table_upstreamDataflow.sql',
    r'sql\create_tables\create_table_datasourceUsage.sql',
    r'sql\create_tables\create_table_endorsementDetails.sql',
    r'sql\create_tables\create_table_measure.sql',
    r'sql\create_tables\create_table_member.sql',
    r'sql\create_tables\create_table_tablePermission.sql',
    r'sql\create_tables\create_table_source.sql',
    r'sql\create_tables\create_table_sensitivityLabel.sql', 
    r'sql\create_tables\create_table_column.sql'
]

for sql_file in sql_create_list:
    # read the sql file
    with open(sql_file, 'r') as f:
        sql_script = f.read()

    # execute script
    cursor.execute(sql_script)
    conn.commit()

# close connection
cursor.close()
conn.close()
