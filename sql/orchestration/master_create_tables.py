"""
Orchestration script to create tables in correct order

NOTE try except with no handling for now
"""
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc
import pandas as pd
from bcpandas import SqlCreds, to_sql
import logging
import yaml

# configure logging
logging.basicConfig(filename='logs\sql_error_log.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# get config values from file
with open('docs\sql_master_create_tables_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# get sql admin credentials
key_vault_name = config['key_vault_name']
secret_name = config['secret_name']

# Construct the Key Vault URL
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a SecretClient
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Retrieve the secret
retrieved_secret = client.get_secret(secret_name)

# define connection string

creds = SqlCreds(
    server=config['sqlCreds']['server'],
    database=config['sqlCreds']['database'],
    username=config['sqlCreds']['username'],
    password=retrieved_secret.value
)

conn_str_2 = f'Driver={"ODBC Driver 17 for SQL Server"};Server=tcp:{config['sqlCreds']['server']},1433;Database={config['sqlCreds']['database']};Uid={config['sqlCreds']['username']};Pwd={retrieved_secret.value};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'
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

# add sql insert list ###########
sql_insert_list = [
    r'data\workspace.csv',
    r'data\dataset.csv',
    r'data\user.csv',
    r'data\expression.csv',
    r'data\table.csv',
    r'data\role.csv',
    r'data\upstreamDataflow.csv',
    r'data\datasourceUsage.csv',
    r'data\endorsementDetails.csv',
    r'data\measure.csv',
    r'data\member.csv',
    r'data\tablePermission.csv',
    r'data\source.csv',
    r'data\sensitivityLabel.csv',
    r'data\column.csv'
]

sql_table_name_list = [
    'workspace',
    'dataset',
    'user_table',
    'expression_table',
    'table_table',
    'role_table',
    'upstreamDataflow',
    'datasourceUsage',
    'endorsementDetails',
    'measure_table',
    'member_table',
    'tablePermission',
    'source_table',
    'sensitivityLabel',
    'column_table'
]

for index, sql_file in enumerate(sql_create_list):
    # read the sql file
    with open(sql_file, 'r') as f:
        sql_script = f.read()

    # execute script
    cursor.execute(sql_script)
    conn.commit()

    # get column names
    table_name = sql_table_name_list[index]
    query = f"""SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}' """
    
    cursor.execute(query)
    column_rows = cursor.fetchall()

    # Convert column_rows to a list of strings
    column_names = [row.COLUMN_NAME for row in column_rows]

    # load files to pandas dataframe
    try:
        df = pd.read_csv(sql_insert_list[index], header=None, names=column_names)
    except Exception as e:
        logging.error(f"Failed to process dataframe for {sql_insert_list[index]} with error {e}")
        continue

    # use bcpandas to load data to sql
    try:
        to_sql(df, sql_table_name_list[index], creds, index=False, if_exists='append')
    except Exception as e:
        logging.error(f"Failed to load data to {sql_table_name_list[index]} with error {e}")
        continue

# close connection
cursor.close()
conn.close()
