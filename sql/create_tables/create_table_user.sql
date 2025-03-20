IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'user_table')
BEGIN
    CREATE TABLE user_table(
        id INT PRIMARY KEY IDENTITY,
        displayName VARCHAR(255) NOT NULL,
        fk_object_id VARCHAR(255) NOT NULL,
        foreignKeyObjectType VARCHAR(255) NOT NULL,
        emailAddress VARCHAR(255) NOT NULL,
        appUserAccessRights VARCHAR(255) NOT NULL,
        identifier VARCHAR(255) NOT NULL,
        graphId VARCHAR(255) NOT NULL,
        principalType VARCHAR(255) NOT NULL,
        userTypeId VARCHAR(255),
        profile VARCHAR(255),

        FOREIGN KEY (fk_object_id) REFERENCES dataset(id),
        CONSTRAINT ck_foreignKeyObjectType_user CHECK (foreignKeyObjectType IN ('workspace', 'dashboard',
        'dataset', 'dataflow','report'))
    );
END