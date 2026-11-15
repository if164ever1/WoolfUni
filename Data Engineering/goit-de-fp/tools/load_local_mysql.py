"""Load the two GoIT CSV snapshots into a disposable local MySQL database."""
import argparse
import csv
import os
from pathlib import Path
import re

import mysql.connector

TABLES = ("athlete_bio", "athlete_event_results")


def import_snapshots(connection, root, database):
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` DEFAULT CHARACTER SET utf8mb4")
        cursor.execute(f"USE `{database}`")
        for table in TABLES:
            with (root / f"{table}.csv").open(encoding="utf-8-sig", newline="") as file:
                reader = csv.reader(file)
                headers = next(reader)
                if not all(re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", field) for field in headers):
                    raise ValueError(f"Unexpected CSV columns in {table}")
                definitions = ", ".join(f"`{field}` TEXT" for field in headers)
                cursor.execute(f"CREATE TABLE `{table}` ({definitions}) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
                placeholders = ", ".join(["%s"] * len(headers))
                statement = f"INSERT INTO `{table}` VALUES ({placeholders})"
                batch = []
                count = 0
                for values in reader:
                    if len(values) != len(headers):
                        raise ValueError(f"Malformed row in {table} at data row {count + len(batch) + 1}")
                    batch.append(tuple(value if value != "" else None for value in values))
                    if len(batch) >= 1000:
                        cursor.executemany(statement, batch)
                        count += len(batch)
                        batch.clear()
                if batch:
                    cursor.executemany(statement, batch)
                    count += len(batch)
                connection.commit()
                print(f"{database}.{table}: imported {count:,} records", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_dir", type=Path)
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--database", default="olympic_dataset")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]{0,63}", args.database):
        parser.error("Invalid database name")
    with mysql.connector.connect(
        host="127.0.0.1", port=args.port,
        user=os.getenv("LOCAL_MYSQL_ADMIN_USER", "root"),
        password=os.getenv("LOCAL_MYSQL_ADMIN_PASSWORD", ""),
        charset="utf8mb4",
    ) as connection:
        import_snapshots(connection, args.csv_dir, args.database)


if __name__ == "__main__":
    main()
