CREATE TABLE [dbo].[notebook_compute_configuration] (
    [notebook_id]     UNIQUEIDENTIFIER NOT NULL,
    [notebook_name]   NVARCHAR (256)   NOT NULL,
    [is_enabled]      BIT              CONSTRAINT [DF_notebook_compute_configuration_is_enabled] DEFAULT ((0)) NOT NULL,
    [driver_memory]   VARCHAR (8)      NULL,
    [driver_cores]    INT              NULL,
    [executor_memory] VARCHAR (8)      NULL,
    [executor_cores]  INT              NULL,
    [num_executors]   INT              NULL,
    [created_at]      DATETIME2 (7)    CONSTRAINT [DF_notebook_compute_configuration_created_at] DEFAULT (sysutcdatetime()) NOT NULL,
    [updated_at]      DATETIME2 (7)    CONSTRAINT [DF_notebook_compute_configuration_updated_at] DEFAULT (sysutcdatetime()) NOT NULL,
    [updated_by]      NVARCHAR (256)   CONSTRAINT [DF_notebook_compute_configuration_updated_by] DEFAULT (suser_sname()) NOT NULL,
    CONSTRAINT [PK_notebook_compute_configuration] PRIMARY KEY CLUSTERED ([notebook_id] ASC),
    CONSTRAINT [CK_notebook_compute_configuration_audit_time] CHECK ([updated_at]>=[created_at]),
    CONSTRAINT [CK_notebook_compute_configuration_driver_cores] CHECK ([driver_cores] IS NULL OR ([driver_cores]=(64) OR [driver_cores]=(32) OR [driver_cores]=(16) OR [driver_cores]=(8) OR [driver_cores]=(4))),
    CONSTRAINT [CK_notebook_compute_configuration_driver_memory] CHECK ([driver_memory] IS NULL OR ([driver_memory]='400g' OR [driver_memory]='224g' OR [driver_memory]='112g' OR [driver_memory]='56g' OR [driver_memory]='28g')),
    CONSTRAINT [CK_notebook_compute_configuration_enabled_complete] CHECK ([is_enabled]=(0) OR [driver_memory] IS NOT NULL AND [driver_cores] IS NOT NULL AND [executor_memory] IS NOT NULL AND [executor_cores] IS NOT NULL AND [num_executors] IS NOT NULL),
    CONSTRAINT [CK_notebook_compute_configuration_executor_cores] CHECK ([executor_cores] IS NULL OR ([executor_cores]=(64) OR [executor_cores]=(32) OR [executor_cores]=(16) OR [executor_cores]=(8) OR [executor_cores]=(4))),
    CONSTRAINT [CK_notebook_compute_configuration_executor_memory] CHECK ([executor_memory] IS NULL OR ([executor_memory]='400g' OR [executor_memory]='224g' OR [executor_memory]='112g' OR [executor_memory]='56g' OR [executor_memory]='28g')),
    CONSTRAINT [CK_notebook_compute_configuration_notebook_name] CHECK (len(ltrim(rtrim([notebook_name])))>(0)),
    CONSTRAINT [CK_notebook_compute_configuration_num_executors] CHECK ([num_executors] IS NULL OR [num_executors]>=(1))
);


GO

