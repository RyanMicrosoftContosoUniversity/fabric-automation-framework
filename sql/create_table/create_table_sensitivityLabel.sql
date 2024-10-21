IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'sensitivityLabel')
BEGIN
    CREATE TABLE sensitivityLabel(
        labelId VARCHAR(255) PRIMARY KEY,
        fk_object_id VARCHAR(255) NOT NULL,
        foreignKeyObjectType VARCHAR(255) NOT NULL,

        CONSTRAINT foreignKeyObjectType CHECK (foreignKeyObjectType IN ('workspace', 'dashboard', 'dataset', 'dataflow', 'datamart'))
    );
END