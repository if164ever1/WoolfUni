"""Stage 2: clean every string column and remove duplicate rows."""
import argparse
import os
from pathlib import Path
import re
import unicodedata

from pyspark.sql import functions as F
from pyspark.sql.types import StringType

import sys

if __package__ in (None, ""):  # SparkSubmitOperator calls this file directly.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from batch.common import TABLES, spark_session


def clean_text(value):
    """Remove control/format characters and collapse whitespace, preserving names."""
    if value is None:
        return None
    safe = "".join(
        char for char in value
        if char in "\t\r\n" or unicodedata.category(char) not in {"Cc", "Cf"}
    )
    return re.sub(r"\s+", " ", safe).strip() or None


clean_text_udf = F.udf(clean_text, StringType())


def run(root):
    spark = spark_session("Olympics Bronze to Silver")
    try:
        for table in TABLES:
            source = spark.read.parquet(str(root / "bronze" / table))
            df = source.select(*(
                clean_text_udf(F.col(field.name)).alias(field.name)
                if isinstance(field.dataType, StringType) else F.col(field.name)
                for field in source.schema.fields
            )).dropDuplicates()
            destination = root / "silver" / table
            df.write.mode("overwrite").parquet(str(destination))
            print(f"SILVER {table}", flush=True)
            spark.read.parquet(str(destination)).show(5, truncate=24)
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(os.getenv("LAKE_ROOT", "lake")))
    run(parser.parse_args().root.resolve())
