"""
Producer script that sends messages to RabbitMQ queue.
"""

import pika
import json
import time
from datetime import datetime
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    QUEUE_NAME,
    MESSAGE_PROPERTIES,
)

def create_connection():
    """Create a connection to RabbitMQ server."""
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

def publish_message(channel, message):
    """Publish a message to the queue."""
    try:
        # Create message with timestamp
        message_body = {
            'content': message,
            'timestamp': datetime.now().isoformat()
        }
        
        # Convert message to JSON
        message_json = json.dumps(message_body)
        
        # Publish message
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=message_json,
            properties=pika.BasicProperties(**MESSAGE_PROPERTIES)
        )
        print(f" [x] Sent message: {message}")
        
    except Exception as e:
        print(f" [!] Error publishing message: {e}")

def main():
    """Main function to run the producer."""
    try:
        # Create connection and channel
        connection = create_connection()
        channel = connection.channel()
        
        # Declare queue
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        
        # Send sample messages
        messages = [
            "Task 1: Process user data",
            "Task 2: Generate report",
            "Task 3: Send notifications",
            "Task 4: Update database",
            "Task 5: Cleanup old records"
        ]
        
        for message in messages:
            publish_message(channel, message)
            time.sleep(1)  # Wait 1 second between messages
        
        # Close connection
        connection.close()
        print("\n [*] Producer finished sending messages")
        
    except pika.exceptions.AMQPConnectionError:
        print(" [!] Could not connect to RabbitMQ server. Is it running?")
    except Exception as e:
        print(f" [!] Unexpected error: {e}")

if __name__ == '__main__':
    main()