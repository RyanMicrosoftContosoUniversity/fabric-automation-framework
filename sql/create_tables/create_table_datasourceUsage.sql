IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'datasourceUsage')
BEGIN
    CREATE TABLE datasourceUsage(
        id INT PRIMARY KEY IDENTITY,
        datasourceInstanceId VARCHAR(255) NOT NULL,
        fk_object_id VARCHAR(255) NOT NULL,
        foreignKeyObjectType VARCHAR(255) NOT NULL,

        CONSTRAINT ck_foreignKeyObjectType_dsUsage CHECK (foreignKeyObjectType IN ('dataflow', 'dataset'))
    );
END