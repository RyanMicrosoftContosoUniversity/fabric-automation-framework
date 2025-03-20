IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'table')
BEGIN
    CREATE TABLE table(
        id INT PRIMARY KEY AUTO_INCREMENT,
        fk_dataset_id INT NOT NULL,
        FOREIGN KEY (fk_dataset_id) REFERENCES dataset(id)
    );
END