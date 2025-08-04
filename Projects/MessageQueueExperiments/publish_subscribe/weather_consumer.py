"""Weather updates consumer implementation."""

from base_consumer import BaseConsumer
from config import WEATHER_QUEUE, WEATHER_PATTERN

class WeatherConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(WEATHER_QUEUE, WEATHER_PATTERN)
    
    def process_message(self, message_data):
        print(f"Weather Update: {message_data['content']}")
        print(f"Location: {message_data['category']}")
        print(f"Time: {message_data['timestamp']}")

if __name__ == '__main__':
    consumer = WeatherConsumer()
    consumer.start_consuming()