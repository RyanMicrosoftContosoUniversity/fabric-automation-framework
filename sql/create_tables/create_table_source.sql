IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'source')
BEGIN
    CREATE TABLE source(
        id INT PRIMARY KEY IDENTITY,
        expression VARCHAR(255) NOT NULL,
        fk_dataset_id INT NOT NULL,
        table_name VARCHAR(255) NOT NULL

  
    );
END