from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_NAME, NUM_PARTITIONS, REPLICATION_FACTOR

def create_multi_partition_topic():
    """Create a topic with multiple partitions"""
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    )

    topic_list = []
    topic_list.append(
        NewTopic(
            name=TOPIC_NAME,
            num_partitions=NUM_PARTITIONS,
            replication_factor=REPLICATION_FACTOR
        )
    )

    try:
        admin_client.create_topics(new_topics=topic_list)
        print(f"Topic {TOPIC_NAME} created successfully with {NUM_PARTITIONS} partitions")
    except TopicAlreadyExistsError:
        print(f"Topic {TOPIC_NAME} already exists")
    finally:
        admin_client.close()

if __name__ == "__main__":
    create_multi_partition_topic()
