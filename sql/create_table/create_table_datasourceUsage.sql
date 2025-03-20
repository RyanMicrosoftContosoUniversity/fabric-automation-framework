IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'datasourceUsage')
BEGIN
    CREATE TABLE datasourceUsage(
        id INT PRIMARY KEY AUTO_INCREMENT,
        datasourceInstanceId VARCHAR(255) NOT NULL,
        fk_object_id VARCHAR(255) NOT NULL,
        foreignKeyObjectType VARCHAR(255) NOT NULL,

        CONSTRAINT foreignKeyObjectType CHECK (foreignKeyObjectType IN ('dataflow', 'dataset'))
    );
END