"""Stage 1: download the original CSV files and convert them to Bronze Parquet."""
import argparse
import os
from pathlib import Path
import shutil
import tempfile
from urllib.request import urlopen

import sys

if __package__ in (None, ""):  # SparkSubmitOperator calls this file directly.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from batch.common import TABLES, require_columns, spark_session

DEFAULT_BASE = "https://ftp.goit.study/neoversity/"


def fetch_csv(base_url, table, landing):
    url = f"{base_url.rstrip('/')}/{table}.csv"
    target = landing / f"{table}.csv"
    # Commit the raw file only after the full body has been downloaded.
    with tempfile.NamedTemporaryFile(dir=landing, delete=False) as raw:
        temporary = Path(raw.name)
        try:
            with urlopen(url, timeout=90) as response:
                shutil.copyfileobj(response, raw)
                expected = response.headers.get("Content-Length")
                if expected and raw.tell() != int(expected):
                    raise IOError(f"Incomplete download: {url}")
            raw.close()
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    return target


def run(root, base_url):
    landing = root / "landing"
    landing.mkdir(parents=True, exist_ok=True)
    spark = spark_session("Olympics Landing to Bronze")
    try:
        for table in TABLES:
            # Preserve the CSV in Landing and parse quoted multiline descriptions.
            raw = fetch_csv(base_url, table, landing)
            df = spark.read.options(header=True, multiLine=True, encoding="UTF-8", escape='"', mode="FAILFAST").csv(str(raw))
            require_columns(df, "athlete_id")
            destination = root / "bronze" / table
            df.write.mode("overwrite").parquet(str(destination))
            print(f"BRONZE {table}", flush=True)
            spark.read.parquet(str(destination)).show(5, truncate=24)
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(os.getenv("LAKE_ROOT", "lake")))
    parser.add_argument("--base-url", default=os.getenv("OLYMPIC_DATA_BASE_URL", DEFAULT_BASE))
    args = parser.parse_args()
    run(args.root.resolve(), args.base_url)
