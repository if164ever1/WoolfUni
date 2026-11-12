from confluent_kafka.admin import AdminClient, NewTopic
from config import BOOTSTRAP_SERVERS, BUILDING_TOPIC, TEMPERATURE_TOPIC, HUMIDITY_TOPIC, SUFFIX

admin_client = AdminClient({"bootstrap.servers": BOOTSTRAP_SERVERS})
existing = set(admin_client.list_topics(timeout=10).topics)
topics = [BUILDING_TOPIC, TEMPERATURE_TOPIC, HUMIDITY_TOPIC]
missing = [NewTopic(name, num_partitions=3, replication_factor=1) for name in topics if name not in existing]
if missing:
    for name, future in admin_client.create_topics(missing).items():
        future.result(timeout=15)
        print(f"Created: {name}")
print("Topics for this homework:")
for topic in sorted(admin_client.list_topics(timeout=10).topics):
    if SUFFIX in topic:
        print(topic)
