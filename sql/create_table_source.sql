CREATE TABLE IF NOT EXISTS source(
    id INT PRIMARY KEY AUTO_INCREMENT,
    expression VARCHAR(255) NOT NULL,
    fk_dataset_id INT NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (fk_dataset_id, table_name) REFERENCES table(table.id)
);