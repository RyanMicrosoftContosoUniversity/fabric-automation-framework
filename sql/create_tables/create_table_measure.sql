IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'measure_table')
BEGIN
    CREATE TABLE measure_table(
        id INT PRIMARY KEY IDENTITY,
        name VARCHAR(255) NOT NULL,
        expression VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        isHidden BIT NOT NULL,
        fk_dataset_id VARCHAR(255) NOT NULL,
        table_name VARCHAR(255) NOT NULL

    );
END