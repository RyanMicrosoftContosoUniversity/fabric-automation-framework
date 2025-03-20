IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'column')
BEGIN
    CREATE TABLE column(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        dataType VARCHAR(255) NOT NULL,
        isHidden BOOLEAN NOT NULL,
        fk_dataset_id INT NOT NULL,
        table_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (fk_dataset_id, table_name) REFERENCES table(table.id)
    );
END