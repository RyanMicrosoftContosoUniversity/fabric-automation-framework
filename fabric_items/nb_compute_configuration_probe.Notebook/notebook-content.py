# Fabric notebook source


# MARKDOWN ********************

# # Fabric Spark compute configuration probe
# 
# Emits one JSON object containing the effective Spark application and compute configuration. This notebook performs no data reads or writes.

# CELL ********************

import json
from datetime import datetime, timezone


spark_conf = spark.sparkContext.getConf()


def get_conf(key):
    value = spark_conf.get(key, None)
    return value if value not in (None, "") else None


def as_int(value):
    return int(value) if value is not None else None


def as_bool(value):
    return value.lower() == "true" if value is not None else None


effective_configuration = {
    "record_type": "fabric_spark_compute_configuration_probe",
    "schema_version": 1,
    "observed_at_utc": datetime.now(timezone.utc).isoformat(),
    "spark_application_id": spark.sparkContext.applicationId,
    "driver_memory": get_conf("spark.driver.memory"),
    "driver_cores": as_int(get_conf("spark.driver.cores")),
    "executor_memory": get_conf("spark.executor.memory"),
    "executor_cores": as_int(get_conf("spark.executor.cores")),
    "executor_instances": as_int(get_conf("spark.executor.instances")),
    "dynamic_allocation_enabled": as_bool(get_conf("spark.dynamicAllocation.enabled")),
    "dynamic_allocation_min_executors": as_int(get_conf("spark.dynamicAllocation.minExecutors")),
    "dynamic_allocation_max_executors": as_int(get_conf("spark.dynamicAllocation.maxExecutors")),
    "default_parallelism": spark.sparkContext.defaultParallelism,
}

effective_json = json.dumps(effective_configuration, sort_keys=True)
print(effective_json)
notebookutils.notebook.exit(effective_json)
