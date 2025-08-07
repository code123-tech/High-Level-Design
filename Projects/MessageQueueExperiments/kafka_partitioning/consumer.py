import json
import threading
from typing import List
from kafka import KafkaConsumer, TopicPartition
from config import CONSUMER_CONFIG, TOPIC_NAME
from colorama import init, Fore

init(autoreset=True)

class MessageConsumer(threading.Thread):
    def __init__(self, consumer_id: str, partitions: List[int] = None):
        super().__init__()
        self.consumer_id = consumer_id
        self.stop_event = threading.Event()
        
        # Create consumer instance
        self.consumer = KafkaConsumer(
            **CONSUMER_CONFIG,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        
        if partitions:
            # Assign specific partitions if provided
            topic_partitions = [TopicPartition(TOPIC_NAME, p) for p in partitions]
            self.consumer.assign(topic_partitions)
        else:
            # Subscribe to topic (will use consumer group for partition assignment)
            self.consumer.subscribe([TOPIC_NAME])
        
        # Get assigned partitions
        self.assigned_partitions = self.consumer.assignment()
        print(f"{Fore.YELLOW}Consumer {consumer_id} assigned partitions: {[p.partition for p in self.assigned_partitions]}")

    def run(self):
        try:
            while not self.stop_event.is_set():
                for message in self.consumer:
                    if self.stop_event.is_set():
                        break
                    
                    print(f"\n{Fore.GREEN}Consumer {self.consumer_id} received:")
                    print(f"Partition: {message.partition}")
                    print(f"Offset: {message.offset}")
                    print(f"Key: {message.key.decode('utf-8') if message.key else None}")
                    print(f"Value: {message.value}")
        finally:
            self.consumer.close()

    def stop(self):
        self.stop_event.set()

def demo_consumer_groups():
    # Create multiple consumers in the same group
    consumers = [
        MessageConsumer(f"consumer_{i}")
        for i in range(3)  # Create 3 consumers
    ]
    
    # Start all consumers
    for consumer in consumers:
        consumer.start()
    
    try:
        # Let consumers run for a while
        input(f"{Fore.CYAN}Press Enter to stop consumers...")
    finally:
        # Stop all consumers
        for consumer in consumers:
            consumer.stop()
        
        # Wait for all consumers to finish
        for consumer in consumers:
            consumer.join()

if __name__ == "__main__":
    demo_consumer_groups()
