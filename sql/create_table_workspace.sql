CREATE TABLE IF NOT EXISTS workspace(
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    isOnDedicatedCapacity BOOLEAN NOT NULL,
    capacityId VARCHAR(255) NOT NULL,
    defaultDatasetStorageFormat VARCHAR(255) NOT NULL
);