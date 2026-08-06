# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5ebdff03-ae40-4e0a-8ed1-c3d209f7f88f",
# META       "default_lakehouse_name": "taxi_bronze",
# META       "default_lakehouse_workspace_id": "896bca78-0d4a-4dc9-8716-05539ecf4ea5"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Bronze — Ingest raw NYC taxi CSV
Lands raw data as-is with audit metadata. Append-only, partitioned by ingestion_date.

# CELL ********************

import uuid
from pyspark.sql.functions import current_timestamp, input_file_name, lit, to_date

batch_id = str(uuid.uuid4())
print('batch_id:', batch_id)


# CELL ********************

df = (spark.read.format('csv')
        .option('header','true')
        .option('inferSchema','true')
        .load('Files/landing/'))

df = (df
      .withColumn('ingestion_timestamp', current_timestamp())
      .withColumn('source_file', input_file_name())
      .withColumn('batch_id', lit(batch_id))
      .withColumn('ingestion_date', to_date(current_timestamp())))


# CELL ********************

(df.write.mode('overwrite')
   .format('delta')
   .partitionBy('ingestion_date')
   .saveAsTable('yellow_trips_raw'))

cnt = spark.table('yellow_trips_raw').count()
print('bronze rows:', cnt)
assert cnt > 0, 'Bronze table is empty'

