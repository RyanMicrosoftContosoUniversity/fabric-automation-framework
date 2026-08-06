# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5103ce50-e64b-42a2-ae36-f97addbafea5",
# META       "default_lakehouse_name": "taxi_gold",
# META       "default_lakehouse_workspace_id": "896bca78-0d4a-4dc9-8716-05539ecf4ea5"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Gold — Aggregate for analytics
Read-optimized (V-Order + Optimize Write). Daily summary + hourly demand for Power BI Direct Lake.

# CELL ********************

spark.conf.set('spark.sql.parquet.vorder.default','true')
spark.conf.set('spark.databricks.delta.optimizeWrite.enabled','true')
spark.conf.set('spark.databricks.delta.optimizeWrite.binSize','1g')


# CELL ********************

ws = '896bca78-0d4a-4dc9-8716-05539ecf4ea5'
silver_tbl = 'abfss://896bca78-0d4a-4dc9-8716-05539ecf4ea5@onelake.dfs.fabric.microsoft.com/3f4085fa-0756-4e9a-95ec-5a767a0553c6/Tables/yellow_trips_clean'
from pyspark.sql.functions import count, sum as ssum, avg, round as sround, hour
s = spark.read.format('delta').load(silver_tbl)
print('silver input rows:', s.count())


# CELL ********************

daily = (s.groupBy('trip_date').agg(
    count('*').alias('trip_count'),
    sround(ssum('total_amount'),2).alias('total_revenue'),
    sround(avg('fare_amount'),2).alias('avg_fare'),
    sround(avg('trip_distance'),2).alias('avg_distance'),
    sround(avg('trip_minutes'),2).alias('avg_trip_minutes'),
    sround(ssum('tip_amount'),2).alias('total_tips')
  ).orderBy('trip_date'))

(daily.write.mode('overwrite').option('overwriteSchema','true')
   .format('delta').saveAsTable('nyc_taxi_daily_summary'))


# CELL ********************

hourly = (s.withColumn('pickup_hour', hour('pickup_ts')).groupBy('pickup_hour').agg(
    count('*').alias('trip_count'),
    sround(avg('total_amount'),2).alias('avg_total')
  ).orderBy('pickup_hour'))

(hourly.write.mode('overwrite').option('overwriteSchema','true')
   .format('delta').saveAsTable('nyc_taxi_hourly_demand'))


# CELL ********************

spark.sql('OPTIMIZE nyc_taxi_daily_summary')
spark.sql('OPTIMIZE nyc_taxi_hourly_demand')
d = spark.table('nyc_taxi_daily_summary').count()
h = spark.table('nyc_taxi_hourly_demand').count()
print('gold daily rows:', d, '| hourly rows:', h)
assert d > 0 and h > 0, 'Gold tables empty'

