IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'role')
BEGIN
    CREATE TABLE role(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        modelPermission VARCHAR(255) NOT NULL,
        fk_dataset_id INT NOT NULL,
        FOREIGN KEY (fk_dataset_id) REFERENCES table(dataset.id)    
    );
END