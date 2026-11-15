"""Stage 3: produce medal-conditioned physical statistics by sport, sex and NOC."""
import argparse
import os
from pathlib import Path

from pyspark.sql import functions as F

import sys

if __package__ in (None, ""):  # SparkSubmitOperator calls this file directly.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from batch.common import GROUP_COLUMNS, athlete_bio, average_stats, joined_results, spark_session


def run(root):
    spark = spark_session("Olympics Silver to Gold")
    try:
        bio = spark.read.parquet(str(root / "silver" / "athlete_bio"))
        events = spark.read.parquet(str(root / "silver" / "athlete_event_results"))
        df = average_stats(joined_results(events, athlete_bio(bio))).withColumn("timestamp", F.current_timestamp())
        destination = root / "gold" / "avg_stats"
        df.write.mode("overwrite").parquet(str(destination))
        print("GOLD avg_stats", flush=True)
        spark.read.parquet(str(destination)).orderBy(*GROUP_COLUMNS).show(12, truncate=False)
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(os.getenv("LAKE_ROOT", "lake")))
    run(parser.parse_args().root.resolve())
