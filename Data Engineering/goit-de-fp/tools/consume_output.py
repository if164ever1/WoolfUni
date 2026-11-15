"""Print a bounded sample from the Kafka output topic."""
import argparse
import os
import time
from uuid import uuid4

from confluent_kafka import Consumer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    topic = os.getenv("KAFKA_OUTPUT_TOPIC", "athlete_avg_stats")
    consumer = Consumer({
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        "group.id": f"olympic-review-{uuid4().hex}",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    })
    count = 0
    try:
        print(f"Kafka output topic: {topic}", flush=True)
        consumer.subscribe([topic])
        end = time.monotonic() + args.timeout
        while count < args.limit and time.monotonic() < end:
            message = consumer.poll(0.5)
            if message is None:
                continue
            if message.error():
                raise RuntimeError(str(message.error()))
            print(f"[partition {message.partition()} · offset {message.offset()}]", flush=True)
            print(message.value().decode("utf-8"), flush=True)
            count += 1
    finally:
        consumer.close()
    if count < args.limit:
        raise SystemExit(f"Read {count} of {args.limit} requested messages before timeout")


if __name__ == "__main__":
    main()
