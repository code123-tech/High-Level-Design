"""Sports news consumer implementation."""

from base_consumer import BaseConsumer
from config import SPORTS_QUEUE, SPORTS_PATTERN

class SportsConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(SPORTS_QUEUE, SPORTS_PATTERN)
    
    def process_message(self, message_data):
        print(f"Sports News: {message_data['content']}")
        print(f"Category: {message_data['category']}")
        print(f"Time: {message_data['timestamp']}")

if __name__ == '__main__':
    consumer = SportsConsumer()
    consumer.start_consuming()