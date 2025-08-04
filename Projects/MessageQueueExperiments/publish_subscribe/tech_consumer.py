"""Tech news consumer implementation."""

from base_consumer import BaseConsumer
from config import TECH_QUEUE, TECH_PATTERN

class TechConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(TECH_QUEUE, TECH_PATTERN)
    
    def process_message(self, message_data):
        print(f"Tech News: {message_data['content']}")
        print(f"Category: {message_data['category']}")
        print(f"Time: {message_data['timestamp']}")

if __name__ == '__main__':
    consumer = TechConsumer()
    consumer.start_consuming()