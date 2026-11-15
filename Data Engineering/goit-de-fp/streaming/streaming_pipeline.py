"""MySQL -> Kafka -> Spark Structured Streaming -> Kafka + MySQL."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructField, StructType

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from batch.common import GROUP_COLUMNS, athlete_bio, average_stats, joined_results, require_columns, spark_session

EVENT_COLUMNS = (
    "edition", "edition_id", "country_noc", "sport", "event", "result_id",
    "athlete", "athlete_id", "pos", "medal", "isTeamSport",
)
EVENT_SCHEMA = StructType([StructField(name, StringType(), True) for name in EVENT_COLUMNS])


def required(name):
    value = os.getenv(name)
    if value is None or (not value and not name.endswith("_PASSWORD")):
        raise ValueError(f"Set {name} in the local environment")
    return value


def kafka_options():
    options = {"kafka.bootstrap.servers": required("KAFKA_BOOTSTRAP_SERVERS")}
    path = os.getenv("SPARK_KAFKA_OPTIONS_FILE")
    if path:
        with open(path, encoding="utf-8") as config:
            extra = json.load(config)
        if not isinstance(extra, dict) or not all(
            key.startswith("kafka.") and isinstance(value, (str, int, float, bool))
            for key, value in extra.items()
        ):
            raise ValueError("Kafka options must be a JSON object with kafka.* names and scalar values")
        options.update(extra)
    return options


def mysql_source(spark, table):
    return (
        spark.read.format("jdbc")
        .option("url", required("SOURCE_JDBC_URL"))
        .option("driver", "com.mysql.cj.jdbc.Driver")
        .option("dbtable", table)
        .option("user", required("SOURCE_MYSQL_USER"))
        .option("password", required("SOURCE_MYSQL_PASSWORD"))
        .load()
    )


def publish_source_events(spark, topic):
    # Етап 3.а): читання athlete_event_results з MySQL і завантаження JSON у Kafka.
    source = mysql_source(spark, "athlete_event_results")
    require_columns(source, *EVENT_COLUMNS)
    payload = source.select(
        F.col("athlete_id").cast("string").alias("key"),
        F.to_json(F.struct(*[F.col(name).cast("string").alias(name) for name in EVENT_COLUMNS]),
                  {"ignoreNullFields": "false"}).alias("value"),
    )
    payload.write.format("kafka").options(**kafka_options()).option("topic", topic).save()
    print(f"Source results published to Kafka topic {topic}", flush=True)


def read_events(spark, topic):
    # Етап 3.б): потокове читання Kafka і перетворення полів JSON на колонки.
    kafka = (
        spark.readStream.format("kafka")
        .options(**kafka_options())
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
    )
    if os.getenv("MAX_OFFSETS_PER_TRIGGER"):
        kafka = kafka.option("maxOffsetsPerTrigger", int(os.environ["MAX_OFFSETS_PER_TRIGGER"]))
    decoded = kafka.load().select(F.from_json(F.col("value").cast("string"), EVENT_SCHEMA).alias("record"))
    return decoded.select("record.*").filter(F.col("athlete_id").isNotNull())


def mysql_connection():
    import mysql.connector

    config = dict(
        host=required("SINK_MYSQL_HOST"),
        port=int(os.getenv("SINK_MYSQL_PORT", "3306")),
        database=required("SINK_MYSQL_DATABASE"),
        user=required("SINK_MYSQL_USER"),
        password=required("SINK_MYSQL_PASSWORD"),
        charset="utf8mb4",
        connection_timeout=15,
    )
    ca = os.getenv("SINK_MYSQL_SSL_CA")
    if ca:
        config.update(ssl_ca=ca, ssl_verify_cert=True, ssl_verify_identity=True)
    return mysql.connector.connect(**config)


def prepare_sink():
    table = os.getenv("SINK_MYSQL_TABLE", "athlete_avg_stats")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]{0,63}", table):
        raise ValueError("Invalid SINK_MYSQL_TABLE")
    with mysql_connection() as connection, connection.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS `{table}` (
                group_id CHAR(64) CHARACTER SET ascii PRIMARY KEY,
                sport VARCHAR(255) NOT NULL, medal VARCHAR(32) NOT NULL,
                sex VARCHAR(32) NOT NULL, country_noc VARCHAR(16) NOT NULL,
                avg_height DOUBLE NOT NULL, avg_weight DOUBLE NOT NULL,
                `timestamp` DATETIME(6) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
    return table


def upsert_mysql(df, table):
    # Етап 6.б): запис результатів у MySQL за стабільним ключем групи.
    statement = f"""
        INSERT INTO `{table}`
            (group_id, sport, medal, sex, country_noc, avg_height, avg_weight, `timestamp`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) AS incoming
        ON DUPLICATE KEY UPDATE
            avg_height=incoming.avg_height, avg_weight=incoming.avg_weight,
            `timestamp`=incoming.`timestamp`
    """
    fields = (
        "group_id", *GROUP_COLUMNS, "avg_height", "avg_weight",
        F.date_format("timestamp", "yyyy-MM-dd HH:mm:ss.SSSSSS").alias("timestamp"),
    )
    with mysql_connection() as connection, connection.cursor() as cursor:
        # toLocalIterator streams the aggregated groups rather than collecting the source events.
        rows = []
        for row in df.select(*fields).toLocalIterator():
            rows.append(tuple(row))
            if len(rows) >= 1000:
                cursor.executemany(statement, rows)
                rows.clear()
        if rows:
            cursor.executemany(statement, rows)
        connection.commit()


def sink_batch(kafka_topic, table):
    def write_batch(batch_df, batch_id):
        timestamp = datetime.now(timezone.utc)
        stats = (
            batch_df.withColumn("timestamp", F.lit(timestamp))
            .withColumn("group_id", F.sha2(F.to_json(F.struct(*GROUP_COLUMNS)), 256))
            .persist()
        )
        try:
            # Materialize and consume the whole batch, including for stateful updates.
            rows = stats.count()
            if rows:
                # Етап 6.а): JSON зі статистикою в окремий вихідний Kafka-топік.
                (
                    stats.select(
                        F.col("group_id").alias("key"),
                        F.to_json(
                            F.struct(*GROUP_COLUMNS, "avg_height", "avg_weight", "timestamp"),
                            {"timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.SSSSSSXXX"},
                        ).alias("value"),
                    )
                    .write.format("kafka").options(**kafka_options()).option("topic", kafka_topic).save()
                )
                upsert_mysql(stats, table)
            print(f"Spark micro-batch {batch_id}: {rows} updated groups", flush=True)
        finally:
            stats.unpersist()

    return write_batch


def stream(spark, source_topic, output_topic, available_now):
    table = prepare_sink()
    # Етап 1: статичний JDBC DataFrame з біологічними даними.
    raw_bio = mysql_source(spark, "athlete_bio")
    # Етап 2: відкидання порожнього, нечислового та невалідного зросту або ваги.
    dimensions = athlete_bio(raw_bio).persist()
    try:
        dimensions.count()
        # Етап 4: stream-static join за athlete_id. Країна береться з результату.
        joined = joined_results(read_events(spark, source_topic), dimensions)
        # Етап 5: стан Spark зберігає накопичувальні середні за чотирма ключами.
        # Timestamp розрахунку додається один раз всередині кожного мікробатчу.
        aggregates = average_stats(joined)
        # Етап 6: foreachBatch розгалужує один мікробатч у два призначення.
        writer = (
            aggregates.writeStream.outputMode("update")
            .option("checkpointLocation", os.getenv("CHECKPOINT_DIR", "./checkpoints/athlete_avg_stats"))
            .foreachBatch(sink_batch(output_topic, table))
        )
        writer = writer.trigger(availableNow=True) if available_now else writer.trigger(processingTime="10 seconds")
        writer.start().awaitTermination()
    finally:
        dimensions.unpersist()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["seed", "stream"])
    parser.add_argument("--available-now", action="store_true", help="Drain available Kafka offsets and stop")
    args = parser.parse_args()
    source_topic = os.getenv("KAFKA_INPUT_TOPIC", "athlete_event_results")
    output_topic = os.getenv("KAFKA_OUTPUT_TOPIC", "athlete_avg_stats")
    if source_topic == output_topic:
        parser.error("Input and output topics must differ")
    spark = spark_session("Olympic Streaming Pipeline")
    try:
        if args.command == "seed":
            publish_source_events(spark, source_topic)
        else:
            stream(spark, source_topic, output_topic, args.available_now)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
