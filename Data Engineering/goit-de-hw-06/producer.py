import argparse
import json
import os
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

parser = argparse.ArgumentParser()
parser.add_argument('--sensor-id', type=int, required=True)
parser.add_argument('--interval', type=float, default=2)
args = parser.parse_args()
producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092'),
    value_serializer=lambda data: json.dumps(data).encode('utf-8'),
)
try:
    while True:
        message = {
            'id': args.sensor_id,
            'temperature': round(random.uniform(15, 45), 2),
            'humidity': round(random.uniform(20, 95), 2),
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }
        producer.send('building_sensors', value=message)
        producer.flush()
        print(message, flush=True)
        time.sleep(args.interval)
except KeyboardInterrupt:
    print('Producer stopped')
finally:
    producer.close()
