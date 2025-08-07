from typing import Dict, Any

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'multi_partition_topic'
NUM_PARTITIONS = 4
REPLICATION_FACTOR = 1

# Producer configurations
PRODUCER_CONFIG: Dict[str, Any] = {
    'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
    'client_id': 'custom_partitioner_producer'
}

# Consumer configurations
CONSUMER_CONFIG: Dict[str, Any] = {
    'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
    'group_id': 'partition_test_group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True
}
