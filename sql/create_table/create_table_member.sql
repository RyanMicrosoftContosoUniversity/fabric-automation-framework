IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'member')
BEGIN
    CREATE TABLE member(
        id INT PRIMARY KEY AUTO_INCREMENT,
        role_name VARCHAR(255) NOT NULL,
        fk_dataset_id INT NOT NULL,
        member_name VARCHAR(255) NOT NULL,
        memberId VARCHAR(255) NOT NULL,
        memberType VARCHAR(255) NOT NULL,
        identityProvider VARCHAR(255) NOT NULL,

        FOREIGN KEY (role_name, fk_dataset_id) REFERENCES table(role.name, role.fk_dataset_id)
    );
END