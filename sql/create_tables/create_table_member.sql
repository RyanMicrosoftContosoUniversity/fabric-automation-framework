IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'member_table')
BEGIN
    CREATE TABLE member_table(
        id INT PRIMARY KEY IDENTITY,
        role_name VARCHAR(255) NOT NULL,
        fk_dataset_id INT NOT NULL,
        member_name VARCHAR(255) NOT NULL,
        memberId VARCHAR(255) NOT NULL,
        memberType VARCHAR(255) NOT NULL,
        identityProvider VARCHAR(255) NOT NULL,

    );
END