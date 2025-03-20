IF NOT EXISTS (SELECT * FROM information_schema.tables WHERE table_name = 'upstreamDataflow')
BEGIN
    CREATE TABLE upstreamDataflow(
        id INT PRIMARY KEY IDENTITY,
        targetDataflowId VARCHAR(255) NOT NULL,
        groupId VARCHAR(255) NOT NULL,
        fk_object_id VARCHAR(255) NOT NULL,
        foreignKeyObjectType VARCHAR(255) NOT NULL,

        FOREIGN KEY (fk_object_id) REFERENCES dataset(id),
        CONSTRAINT ck_foreignKeyObjectType_upstreamDataflow CHECK (foreignKeyObjectType IN ('dataset', 'datamart'))
    );
END