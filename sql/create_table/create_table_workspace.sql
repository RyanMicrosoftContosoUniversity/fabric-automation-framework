IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'workspace')
BEGIN
    CREATE TABLE workspace (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        isOnDedicatedCapacity BIT NOT NULL,
        capacityId VARCHAR(255) NOT NULL,
        defaultDatasetStorageFormat VARCHAR(255) NOT NULL
    );
END