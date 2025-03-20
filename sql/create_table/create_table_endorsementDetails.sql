IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'endorsementDetails')
BEGIN
    CREATE TABLE endorsementDetails(
        id INT PRIMARY KEY AUTO_INCREMENT,
        fk_object_id VARCHAR(255) NOT NULL,
        foreignKeyObjectType VARCHAR(255) NOT NULL,
        endorsement VARCHAR(255) NOT NULL,
        certifiedBy VARCHAR(255) NOT NULL,

        CONSTRAINT foreignKeyObjectType CHECK (foreignKeyObjectType IN ('dataflow', 'datamart', 'report', 'dataset'))
    );
END