IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'measure')
BEGIN
    CREATE TABLE measure(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        expression VARCHAR(255) NOT NULL,
        description VARCHAR(255) NOT NULL,
        isHidden BOOLEAN NOT NULL,
        fk_dataset_id INT NOT NULL,
        table_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (fk_dataset_id, table_name) REFERENCES table(table.id)
    );
END