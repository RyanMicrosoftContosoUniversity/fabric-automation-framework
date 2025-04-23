CREATE TABLE apiOrchestration (
    id INT IDENTITY(1,1) PRIMARY KEY,
    pipelineName VARCHAR(255),
    source VARCHAR(255),
    kvName VARCHAR(255),
    secretName VARCHAR(255),
    baseURL VARCHAR(255),
    api VARCHAR(255),
    kvArgs VARCHAR(MAX),
    loadType VARCHAR(11) CHECK (loadType IN ('full', 'incremental'))
);


CREATE TABLE pipelineStats (
    runId INT IDENTITY(1,1) PRIMARY KEY,
    apiOrchId INT,
    totalSeconds FLOAT,
    totalBytes BIGINT,
    startTime DATETIME,
    stopTime DATETIME,
    targetFileName NVARCHAR(MAX),
    pipelineStatus NVARCHAR(10) CHECK (pipelineStatus IN ('complete', 'fail')),
    runBy NVARCHAR(MAX),
    FOREIGN KEY (apiOrchId) REFERENCES apiOrchestration(id)
);