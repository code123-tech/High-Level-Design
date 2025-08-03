"""
Consumer script that receives messages from RabbitMQ queue.
"""

import pika
import json
import time
from config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    QUEUE_NAME
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

def process_message(message):
    """
    Process the received message.
    In a real application, this would contain your business logic.
    """
    try:
        # Parse JSON message
        message_data = json.loads(message)
        
        # Extract message content and timestamp
        content = message_data['content']
        timestamp = message_data['timestamp']
        
        # Simulate processing time
        print(f" [x] Processing message: {content}")
        print(f" [x] Message timestamp: {timestamp}")
        time.sleep(2)  # Simulate work being done
        
        print(f" [✓] Finished processing: {content}\n")
        return True
        
    except json.JSONDecodeError:
        print(" [!] Error: Invalid JSON message")
        return False
    except KeyError:
        print(" [!] Error: Invalid message format")
        return False
    except Exception as e:
        print(f" [!] Error processing message: {e}")
        return False

def callback(ch, method, properties, body):
    """Callback function for handling received messages."""
    try:
        message = body.decode()
        success = process_message(message)
        
        if success:
            # Acknowledge message only if processing was successful
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Reject message if processing failed
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
    except Exception as e:
        print(f" [!] Error in callback: {e}")
        # Reject message in case of unexpected errors
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    """Main function to run the consumer."""
    try:
        # Create connection and channel
        connection = create_connection()
        channel = connection.channel()
        
        # Declare queue
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        
        # Set QoS to handle one message at a time
        channel.basic_qos(prefetch_count=1)
        
        # Set up consumer
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
        
        # Start consuming
        channel.start_consuming()
        
    except pika.exceptions.AMQPConnectionError:
        print(" [!] Could not connect to RabbitMQ server. Is it running?")
    except KeyboardInterrupt:
        print(" [*] Consumer stopped by user")
    except Exception as e:
        print(f" [!] Unexpected error: {e}")

if __name__ == '__main__':
    main()