IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'column_table')
BEGIN
    CREATE TABLE column_table(
        id INT PRIMARY KEY IDENTITY,
        name VARCHAR(255) NOT NULL,
        dataType VARCHAR(255) NOT NULL,
        isHidden BIT NOT NULL,
        fk_dataset_id INT NOT NULL,
        table_name VARCHAR(255) NOT NULL


    );
END