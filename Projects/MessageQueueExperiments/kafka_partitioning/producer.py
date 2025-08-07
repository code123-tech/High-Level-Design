import json
import time
from typing import Optional
from kafka import KafkaProducer
from custom_partitioner import RoundRobinPartitioner, KeyBasedPartitioner
from config import PRODUCER_CONFIG, TOPIC_NAME
from colorama import init, Fore

init(autoreset=True)

class MessageProducer:
    def __init__(self, partitioner_type: str = "default"):
        config = PRODUCER_CONFIG.copy()
        
        if partitioner_type == "round_robin":
            config['partitioner'] = RoundRobinPartitioner()
        elif partitioner_type == "key_based":
            config['partitioner'] = KeyBasedPartitioner()
            
        self.producer = KafkaProducer(
            **config,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None
        )

    def send_message(self, message: dict, key: Optional[str] = None):
        future = self.producer.send(TOPIC_NAME, value=message, key=key)
        try:
            record_metadata = future.get(timeout=10)
            print(f"{Fore.GREEN}Message sent successfully to:")
            print(f"Topic: {record_metadata.topic}")
            print(f"Partition: {record_metadata.partition}")
            print(f"Offset: {record_metadata.offset}")
            print(f"Key: {key}")
            print(f"Message: {message}\n")
        except Exception as e:
            print(f"{Fore.RED}Error sending message: {str(e)}")

    def close(self):
        self.producer.close()

def demo_different_partitioning():
    # Demo with default partitioner
    print(f"{Fore.CYAN}Testing Default Partitioner:")
    producer = MessageProducer("default")
    for i in range(5):
        message = {"message_id": i, "content": f"Default partitioner message {i}"}
        producer.send_message(message)
    producer.close()
    
    time.sleep(1)
    
    # Demo with round-robin partitioner
    print(f"\n{Fore.CYAN}Testing Round Robin Partitioner:")
    producer = MessageProducer("round_robin")
    for i in range(5):
        message = {"message_id": i, "content": f"Round robin message {i}"}
        producer.send_message(message)
    producer.close()
    
    time.sleep(1)
    
    # Demo with key-based partitioner
    print(f"\n{Fore.CYAN}Testing Key-Based Partitioner:")
    producer = MessageProducer("key_based")
    keys = ["user1", "user2", "user1", "user2", "user1"]
    for i, key in enumerate(keys):
        message = {"message_id": i, "content": f"Key-based message {i}"}
        producer.send_message(message, key)
    producer.close()

if __name__ == "__main__":
    demo_different_partitioning()
