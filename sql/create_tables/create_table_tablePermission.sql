IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'tablePermission')
BEGIN
    CREATE TABLE tablePermission(
        id INT PRIMARY KEY IDENTITY,
        role_name VARCHAR(255) NOT NULL,
        fk_dataset_id VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        filterExpression VARCHAR(255) NOT NULL
    );
END