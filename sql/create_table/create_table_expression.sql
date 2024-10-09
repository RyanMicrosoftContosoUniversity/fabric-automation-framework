IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'expression')
BEGIN
    CREATE TABLE expression(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        expression VARCHAR(255) NOT NULL,
        fk_dataset_id INT NOT NULL,

        FOREIGN KEY (fk_dataset_id) REFERENCES dataset(id)
    );
END