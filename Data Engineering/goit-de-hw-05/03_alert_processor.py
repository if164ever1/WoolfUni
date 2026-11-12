import json
from datetime import datetime, timezone
from confluent_kafka import Consumer, Producer, KafkaException
from config import BOOTSTRAP_SERVERS, BUILDING_TOPIC, TEMPERATURE_TOPIC, HUMIDITY_TOPIC

consumer = Consumer({
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": "ihor-sensor-processor",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})
producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS})

def delivery_callback(err, msg):
    if err:
        print(f"ALERT DELIVERY FAILED: {err}", flush=True)
    else:
        print(f"ALERT SENT topic={msg.topic()} partition={msg.partition()} offset={msg.offset()}", flush=True)

def send_alert(topic, data, message):
    alert = {
        "sensor_id": data["sensor_id"],
        "timestamp": data["timestamp"],
        "alert_timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "message": message,
    }
    print(f"FILTERED {topic}: {json.dumps(alert)}", flush=True)
    producer.produce(topic, key=str(data["sensor_id"]).encode(), value=json.dumps(alert).encode(), callback=delivery_callback)
    producer.poll(0)

consumer.subscribe([BUILDING_TOPIC])
print(f"Listening on {BUILDING_TOPIC}. Ctrl+C to stop.", flush=True)
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        try:
            data = json.loads(msg.value())
            temperature = float(data["temperature"])
            humidity = float(data["humidity"])
            if not 25 <= temperature <= 45 or not 15 <= humidity <= 85:
                print(f"SKIPPED out-of-range sensor data: {data}", flush=True)
                consumer.commit(message=msg, asynchronous=False)
                continue
            print(f"RECEIVED sensor={data['sensor_id']} temperature={temperature} humidity={humidity}", flush=True)
            if temperature > 40:
                send_alert(TEMPERATURE_TOPIC, data, "Temperature exceeds 40°C")
            if humidity > 80 or humidity < 20:
                send_alert(HUMIDITY_TOPIC, data, "Humidity outside permitted range (20%-80%)")
            remaining = producer.flush(10)
            if remaining:
                raise RuntimeError(f"{remaining} alert(s) not delivered; offset not committed")
            consumer.commit(message=msg, asynchronous=False)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            print(f"INVALID MESSAGE: {exc}; payload={msg.value()!r}", flush=True)
            consumer.commit(message=msg, asynchronous=False)
except KeyboardInterrupt:
    print("Stopping processor...", flush=True)
finally:
    producer.flush(10)
    consumer.close()
