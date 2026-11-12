import json
from confluent_kafka import Consumer, KafkaException
from config import BOOTSTRAP_SERVERS, TEMPERATURE_TOPIC, HUMIDITY_TOPIC

consumer = Consumer({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": "ihor-alert-viewer",
    "auto.offset.reset": "earliest",
})
consumer.subscribe([TEMPERATURE_TOPIC, HUMIDITY_TOPIC])
print(f"Listening for alerts: {TEMPERATURE_TOPIC}, {HUMIDITY_TOPIC}", flush=True)
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        alert = json.loads(msg.value())
        print(f"[{msg.topic()}] sensor={alert['sensor_id']} time={alert['timestamp']} "
              f"temperature={alert['temperature']}°C humidity={alert['humidity']}% "
              f"ALERT: {alert['message']}", flush=True)
except KeyboardInterrupt:
    print("Stopping viewer...", flush=True)
finally:
    consumer.close()
