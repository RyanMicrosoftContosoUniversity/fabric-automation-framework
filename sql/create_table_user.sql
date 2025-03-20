CREATE TABLE IF NOT EXISTS user(
    id INT PRIMARY KEY AUTO_INCREMENT,
    displayName VARCHAR(255) NOT NULL,
    fk_object_id INT NOT NULL,
    foreignKeyObjectType VARCHAR(255) NOT NULL,
    emailAddress VARCHAR(255) NOT NULL,
    appUserAccessRights VARCHAR(255) NOT NULL,
    identifier VARCHAR(255) NOT NULL,
    graphId VARCHAR(255) NOT NULL,
    principalType VARCHAR(255) NOT NULL,
    userTypeId VARCHAR(255),
    profile VARCHAR(255),

    FOREIGN KEY (fk_object_id) REFERENCES table(dataset.id),
    CONSTRAINT foreignKeyObjectType CHECK (foreignKeyObjectType IN ('workspace', 'dashboard',
     'dataset', 'dataflow','report'))
);