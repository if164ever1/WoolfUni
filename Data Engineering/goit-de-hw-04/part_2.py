"""HW04 part 2: two collect() actions, no cache."""
from pathlib import Path
from pyspark.sql import SparkSession

DATA_PATH = Path(__file__).resolve().parent / "nuek-vuh3.csv"

if not DATA_PATH.is_file():
    raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")

spark = (
    SparkSession.builder
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "2")
    .appName("GoIT-HW04-Part2")
    .getOrCreate()
)

try:
    nuek_df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(DATA_PATH))
    )

    nuek_repart = nuek_df.repartition(2)
    nuek_processed = (
        nuek_repart
        .where("final_priority < 3")
        .select("unit_id", "final_priority")
        .groupBy("unit_id")
        .count()
    )

    intermediate_result = nuek_processed.collect()
    print(f"Part 2: intermediate collect returned {len(intermediate_result)} rows.")

    nuek_processed = nuek_processed.where("count > 2")
    result = nuek_processed.collect()
    print(f"Part 2: final collect returned {len(result)} rows.")
    input("Open http://localhost:4040/jobs/ and take a screenshot. Press Enter to stop Spark...")
finally:
    spark.stop()
