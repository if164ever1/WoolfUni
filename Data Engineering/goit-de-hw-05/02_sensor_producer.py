import argparse
import json
import random
import time
import uuid
from datetime import datetime, timezone
from confluent_kafka import Producer
from config import BOOTSTRAP_SERVERS, BUILDING_TOPIC

parser = argparse.ArgumentParser()
parser.add_argument("--sensor-id", default=None, help="Optional fixed sensor ID")
parser.add_argument("--interval", type=float, default=2.0)
args = parser.parse_args()
if args.interval <= 0:
    parser.error("--interval must be positive")
sensor_id = args.sensor_id or f"sensor-{uuid.uuid4().hex[:8]}"
producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS, "client.id": sensor_id})

def delivered(err, msg):
    if err:
        print(f"Delivery failed: {err}", flush=True)
    else:
        print(f"SENT sensor={sensor_id} topic={msg.topic()} partition={msg.partition()} offset={msg.offset()}", flush=True)

print(f"Sensor started: {sensor_id}. Press Ctrl+C to stop.", flush=True)
try:
    while True:
        payload = {
            "sensor_id": sensor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": round(random.uniform(25, 45), 2),
            "humidity": round(random.uniform(15, 85), 2),
        }
        print(f"GENERATED {json.dumps(payload)}", flush=True)
        producer.produce(BUILDING_TOPIC, key=sensor_id.encode(), value=json.dumps(payload).encode(), callback=delivered)
        producer.poll(0)
        time.sleep(args.interval)
except KeyboardInterrupt:
    print("Stopping sensor...", flush=True)
finally:
    producer.flush(10)
