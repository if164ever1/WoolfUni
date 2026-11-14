import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, coalesce, from_json, lit, struct, to_json, window
from pyspark.sql.types import DoubleType, IntegerType, StringType, StructField, StructType, TimestampType

bootstrap = os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092')
rules_path = os.getenv('ALERTS_CSV', 'alerts_conditions.csv')
checkpoint = os.getenv('CHECKPOINT_DIR', './checkpoint_alerts')
spark = SparkSession.builder.appName('IoT-Spark-Streaming-Alerts').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

sensor_schema = StructType([
    StructField('id', IntegerType()),
    StructField('temperature', DoubleType()),
    StructField('humidity', DoubleType()),
    StructField('timestamp', TimestampType()),
])

# Official homework CSV is expected to have the columns below.
# If its headers differ, normalize them here after inspecting the downloaded CSV.
required = {'id', 'humidity_min', 'humidity_max', 'temperature_min', 'temperature_max', 'code', 'message'}
try:
    rules = spark.read.option('header', True).option('inferSchema', True).csv(rules_path)
except Exception as exc:
    sys.exit(f'Cannot read alert conditions CSV at {rules_path}: {exc}')

# Some course versions use alert_code / alert_message instead of code / message.
for old, new in [('alert_code', 'code'), ('alert_message', 'message')]:
    if old in rules.columns and new not in rules.columns:
        rules = rules.withColumnRenamed(old, new)

# Rules often have no id; generate a stable rule identifier when absent.
required.discard('id')
missing = required - set(rules.columns)
if missing:
    sys.exit(f'CSV missing columns: {sorted(missing)}. Actual columns: {rules.columns}')

for name in ('humidity_min', 'humidity_max', 'temperature_min', 'temperature_max'):
    rules = rules.withColumn(name, col(name).cast('double'))
rules = rules.cache()
print('Alert conditions:')
rules.show(truncate=False)

raw = (spark.readStream.format('kafka')
    .option('kafka.bootstrap.servers', bootstrap)
    .option('subscribe', 'building_sensors')
    .option('startingOffsets', 'earliest')
    .load())

sensors = (raw.select(from_json(col('value').cast('string'), sensor_schema).alias('s'))
    .select('s.*')
    .filter(col('id').isNotNull() & col('timestamp').isNotNull()
            & col('temperature').isNotNull() & col('humidity').isNotNull()))

# Group by sensor so each device is evaluated independently.
aggregated = (sensors.withWatermark('timestamp', '10 seconds')
    .groupBy(window(col('timestamp'), '1 minute', '30 seconds'), col('id'))
    .agg(avg('temperature').alias('avg_temperature'),
         avg('humidity').alias('avg_humidity')))

# -999 indicates an inactive threshold. Active minimum/maximum bounds
# are combined as a valid interval, and violations produce an alert.
temp_violation = (
    ((col('temperature_min') != -999) & (col('avg_temperature') < col('temperature_min')))
    | ((col('temperature_max') != -999) & (col('avg_temperature') > col('temperature_max')))
)
humidity_violation = (
    ((col('humidity_min') != -999) & (col('avg_humidity') < col('humidity_min')))
    | ((col('humidity_max') != -999) & (col('avg_humidity') > col('humidity_max')))
)

# A rule with both temperature and humidity criteria requires both
# dimensions to violate their respective configured ranges.
temp_enabled = (col('temperature_min') != -999) | (col('temperature_max') != -999)
humidity_enabled = (col('humidity_min') != -999) | (col('humidity_max') != -999)
condition = ((~temp_enabled | temp_violation) & (~humidity_enabled | humidity_violation)
             & (temp_enabled | humidity_enabled))

alerts = (aggregated.crossJoin(rules).filter(condition)
    .select(col('id').alias('sensor_id'), col('window.start').alias('window_start'),
            col('window.end').alias('window_end'), 'avg_temperature',
            'avg_humidity', 'code', 'message'))

def publish_batch(batch, batch_id):
    if batch.isEmpty():
        print(f'Batch {batch_id}: no alerts', flush=True)
        return
    print(f'Batch {batch_id}: alerts', flush=True)
    batch.show(truncate=False)
    outgoing = batch.select(
        col('sensor_id').cast('string').alias('key'),
        to_json(struct(*[col(c) for c in batch.columns])).alias('value'))
    (outgoing.write.format('kafka')
        .option('kafka.bootstrap.servers', bootstrap)
        .option('topic', 'building_sensors_alerts')
        .save())

query = (alerts.writeStream.outputMode('append')
    .foreachBatch(publish_batch)
    .option('checkpointLocation', checkpoint)
    .trigger(processingTime='10 seconds')
    .start())
query.awaitTermination()
