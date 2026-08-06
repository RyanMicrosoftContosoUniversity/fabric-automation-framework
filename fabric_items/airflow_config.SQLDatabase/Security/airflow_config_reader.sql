CREATE ROLE [airflow_config_reader]
    AUTHORIZATION [dbo];


GO

ALTER ROLE [airflow_config_reader] ADD MEMBER [fabric_conn];


GO

