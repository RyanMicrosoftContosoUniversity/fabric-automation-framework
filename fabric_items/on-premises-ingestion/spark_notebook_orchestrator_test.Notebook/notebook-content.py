# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

import json

conf = spark.sparkContext.getConf()

def get_conf(key):
    return conf.get(key, None)

compute = {
    "application_id": spark.sparkContext.applicationId,
    "driver_memory": get_conf("spark.driver.memory"),
    "driver_cores": get_conf("spark.driver.cores"),
    "executor_memory": get_conf("spark.executor.memory"),
    "executor_cores": get_conf("spark.executor.cores"),
    "executor_instances": get_conf("spark.executor.instances"),
    "dynamic_allocation_enabled": get_conf("spark.dynamicAllocation.enabled"),
    "dynamic_allocation_min_executors": get_conf(
        "spark.dynamicAllocation.minExecutors"
    ),
    "dynamic_allocation_max_executors": get_conf(
        "spark.dynamicAllocation.maxExecutors"
    ),
    "default_parallelism": spark.sparkContext.defaultParallelism,
}

print(json.dumps(compute, indent=2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
