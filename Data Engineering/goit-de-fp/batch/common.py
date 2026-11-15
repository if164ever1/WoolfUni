"""Shared Spark transforms for the batch and streaming jobs."""
import os

from pyspark.sql import SparkSession, functions as F

TABLES = ("athlete_bio", "athlete_event_results")
GROUP_COLUMNS = ("sport", "medal", "sex", "country_noc")


def spark_session(name):
    spark = (
        SparkSession.builder.appName(name)
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", os.getenv("SPARK_SHUFFLE_PARTITIONS", "4"))
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def require_columns(df, *columns):
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing input columns: {', '.join(sorted(missing))}")


def normalize_text(column):
    return F.trim(F.regexp_replace(column.cast("string"), r"(?U)\s+", " "))


def athlete_bio(df):
    """Keep one usable bio per athlete. Resolve conflicting bios deterministically."""
    require_columns(df, "athlete_id", "sex", "height", "weight")
    dimensions = df.select(
        normalize_text(F.col("athlete_id")).alias("athlete_id"),
        normalize_text(F.col("sex")).alias("sex"),
        F.expr("try_cast(trim(cast(height as string)) as double)").alias("height"),
        F.expr("try_cast(trim(cast(weight as string)) as double)").alias("weight"),
    )
    for field in ("height", "weight"):
        value = F.col(field)
        dimensions = dimensions.filter(value.isNotNull() & (~F.isnan(value)) & (value > 0) & (value < F.lit(float("inf"))))
    return (
        dimensions.filter((F.col("athlete_id") != "") & (F.col("sex") != ""))
        .groupBy("athlete_id")
        .agg(F.min(F.struct("sex", "height", "weight")).alias("bio"))
        .select("athlete_id", "bio.*")
    )


def joined_results(events, bio):
    require_columns(events, "athlete_id", "sport", "medal", "country_noc")
    medal = normalize_text(F.col("medal"))
    event_fields = events.select(
        normalize_text(F.col("athlete_id")).alias("athlete_id"),
        normalize_text(F.col("sport")).alias("sport"),
        F.when(medal.isNull() | F.lower(medal).isin("", "na", "n/a", "none", "null", "no medal"), F.lit("No medal"))
        .otherwise(medal).alias("medal"),
        F.upper(normalize_text(F.col("country_noc"))).alias("country_noc"),
    )
    return event_fields.filter((F.col("sport") != "") & (F.col("country_noc") != "")).join(bio, "athlete_id", "inner")


def average_stats(joined):
    return joined.groupBy(*GROUP_COLUMNS).agg(
        F.avg("height").alias("avg_height"),
        F.avg("weight").alias("avg_weight"),
    )
