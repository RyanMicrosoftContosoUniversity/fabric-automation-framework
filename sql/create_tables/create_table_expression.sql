IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'expression_table')
BEGIN
    CREATE TABLE expression_table(
        id INT PRIMARY KEY IDENTITY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        expression VARCHAR(255) NOT NULL,
        fk_dataset_id VARCHAR(255) NOT NULL,

        FOREIGN KEY (fk_dataset_id) REFERENCES dataset(id)
    );
END