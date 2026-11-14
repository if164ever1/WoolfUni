import os
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

bootstrap = os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092')
admin = KafkaAdminClient(bootstrap_servers=bootstrap)
for name in ('building_sensors', 'building_sensors_alerts'):
    try:
        admin.create_topics([NewTopic(name=name, num_partitions=2, replication_factor=1)])
        print('Created:', name)
    except TopicAlreadyExistsError:
        print('Already exists:', name)
admin.close()
