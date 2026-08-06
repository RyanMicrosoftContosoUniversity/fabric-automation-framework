# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "3f4085fa-0756-4e9a-95ec-5a767a0553c6",
# META       "default_lakehouse_name": "taxi_silver",
# META       "default_lakehouse_workspace_id": "896bca78-0d4a-4dc9-8716-05539ecf4ea5"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Silver — Clean & conform
Deduplicate, drop invalid rows, snake_case schema, derive trip_minutes. Partitioned by trip_date.

# CELL ********************

ws = '896bca78-0d4a-4dc9-8716-05539ecf4ea5'
bronze_tbl = 'abfss://896bca78-0d4a-4dc9-8716-05539ecf4ea5@onelake.dfs.fabric.microsoft.com/5ebdff03-ae40-4e0a-8ed1-c3d209f7f88f/Tables/yellow_trips_raw'


# CELL ********************

from pyspark.sql.functions import col, to_date, unix_timestamp, round as sround

raw = spark.read.format('delta').load(bronze_tbl)
print('bronze input rows:', raw.count())


# CELL ********************

clean = (raw
  .dropDuplicates(['VendorID','tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID','DOLocationID','total_amount'])
  .filter((col('trip_distance') > 0) & (col('passenger_count') > 0) & (col('fare_amount') >= 0))
  .withColumn('pickup_ts', col('tpep_pickup_datetime').cast('timestamp'))
  .withColumn('dropoff_ts', col('tpep_dropoff_datetime').cast('timestamp'))
  .withColumn('trip_date', to_date(col('tpep_pickup_datetime').cast('timestamp')))
  .withColumn('trip_minutes', sround((unix_timestamp('dropoff_ts') - unix_timestamp('pickup_ts'))/60.0, 2))
  .filter(col('trip_minutes') > 0))


# CELL ********************

clean = clean.selectExpr(
  'VendorID as vendor_id','pickup_ts','dropoff_ts','trip_date',
  'passenger_count','trip_distance',
  'PULocationID as pu_location_id','DOLocationID as do_location_id','payment_type',
  'fare_amount','tip_amount','tolls_amount','total_amount','trip_minutes')


# CELL ********************

(clean.write.mode('overwrite')
   .option('overwriteSchema','true')
   .format('delta')
   .partitionBy('trip_date')
   .saveAsTable('yellow_trips_clean'))

spark.sql('OPTIMIZE yellow_trips_clean')
cnt = spark.table('yellow_trips_clean').count()
print('silver rows:', cnt)
assert cnt > 0, 'Silver table is empty'

