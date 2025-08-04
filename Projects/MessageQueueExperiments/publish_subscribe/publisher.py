"""Publisher that sends messages to different topics."""

import pika
import json
from datetime import datetime
import random
import time
from config import *

def create_connection():
    """Create a connection to RabbitMQ server."""
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

def setup_exchange(channel):
    """Setup the topic exchange."""
    channel.exchange_declare(
        exchange=TOPIC_EXCHANGE,
        exchange_type='topic',
        durable=True
    )

def publish_message(channel, routing_key, message):
    """Publish a message to a specific topic."""
    try:
        message_body = {
            'content': message,
            'timestamp': datetime.now().isoformat(),
            'category': routing_key
        }
        
        channel.basic_publish(
            exchange=TOPIC_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message_body),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        print(f" [x] Sent {routing_key}: {message}")
    except Exception as e:
        print(f" [!] Error publishing message: {e}")

def generate_sample_messages():
    """Generate sample messages for different topics."""
    topics = {
        'sports.football': [
            'Manchester United wins 2-1',
            'New transfer deadline approaching',
            'Player injury update'
        ],
        'sports.basketball': [
            'Lakers vs Warriors highlights',
            'NBA draft updates',
            'Player trade news'
        ],
        'tech.mobile': [
            'New smartphone launch',
            'iOS update released',
            'Android security patch'
        ],
        'tech.ai': [
            'New AI model breakthrough',
            'Machine learning advances',
            'AI ethics discussion'
        ],
        'weather.london': [
            'Rain expected tomorrow',
            'Temperature drop alert',
            'Sunny weekend ahead'
        ],
        'weather.newyork': [
            'Storm warning issued',
            'High humidity levels',
            'Clear skies expected'
        ]
    }
    return topics

def main():
    """Main function to run the publisher."""
    try:
        # Create connection and channel
        connection = create_connection()
        channel = connection.channel()
        
        # Setup exchange
        setup_exchange(channel)
        
        # Get sample messages
        topics = generate_sample_messages()
        
        # Publish messages
        while True:
            # Randomly select a topic and message
            topic = random.choice(list(topics.keys()))
            message = random.choice(topics[topic])
            
            publish_message(channel, topic, message)
            time.sleep(2)  # Wait 2 seconds between messages
            
    except KeyboardInterrupt:
        print("\n [*] Publisher stopped by user")
    except Exception as e:
        print(f" [!] Unexpected error: {e}")
    finally:
        if connection and not connection.is_closed:
            connection.close()

if __name__ == '__main__':
    main()