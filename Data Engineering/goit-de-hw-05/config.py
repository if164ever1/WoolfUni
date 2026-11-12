import os
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
SUFFIX = os.getenv("KAFKA_TOPIC_SUFFIX", "ihor")
BUILDING_TOPIC = f"building_sensors_{SUFFIX}"
TEMPERATURE_TOPIC = f"temperature_alerts_{SUFFIX}"
HUMIDITY_TOPIC = f"humidity_alerts_{SUFFIX}"
