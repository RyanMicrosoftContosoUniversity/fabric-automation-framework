IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table_table')
BEGIN
    CREATE TABLE table_table(
        id INT PRIMARY KEY IDENTITY,
        name VARCHAR(255) NOT NULL,
        modelPermission VARCHAR(255) NOT NULL,
        fk_dataset_id VARCHAR(255) NOT NULL,

        FOREIGN KEY (fk_dataset_id) REFERENCES dataset(id)
    );
END