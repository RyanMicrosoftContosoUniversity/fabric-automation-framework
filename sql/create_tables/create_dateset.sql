IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'dataset')
BEGIN
    CREATE TABLE dataset(
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        workspaceId VARCHAR(255) NOT NULL,

        FOREIGN KEY (workspaceId) REFERENCES workspace(id)
    );
END