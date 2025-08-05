"""Slow consumer processing messages at a controlled rate."""

import pika
import json
import time
from datetime import datetime
from monitor import monitor
from config import *

class SlowConsumer:
    def __init__(self):
        self.processed_count = 0
        self.last_process_time = time.time()
        
    def create_connection(self):
        """Create a connection to RabbitMQ."""
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # Declare queue
        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True,
            arguments={
                'x-max-length': MAX_QUEUE_SIZE,
                'x-overflow': 'reject-publish'
            }
        )
        
        # Set QoS
        channel.basic_qos(prefetch_count=PREFETCH_COUNT)
        
        return connection, channel
    
    def process_message(self, message_data):
        """Simulate message processing with controlled speed."""
        try:
            # Calculate time since last message
            current_time = time.time()
            time_diff = current_time - self.last_process_time
            
            # If processing too fast, sleep to maintain rate
            if time_diff < (1 / CONSUMER_RATE):
                time.sleep((1 / CONSUMER_RATE) - time_diff)
            
            # Simulate processing work
            time.sleep(PROCESSING_TIME)
            
            self.processed_count += 1
            self.last_process_time = time.time()
            
            # Record metrics
            monitor.increment_message_out()
            processing_time = (time.time() - current_time) * 1000  # Convert to ms
            monitor.record_latency(processing_time)
            
            if self.processed_count % 100 == 0:
                print(f" [*] Processed {self.processed_count} messages")
                
        except Exception as e:
            print(f" [!] Error processing message: {e}")
            raise
    
    def callback(self, ch, method, properties, body):
        """Callback for message processing."""
        try:
            message = json.loads(body)
            
            # Calculate message age
            message_timestamp = datetime.fromisoformat(message['timestamp'])
            age = (datetime.now() - message_timestamp).total_seconds() * 1000  # ms
            
            print(f" [x] Processing message {message['id']} (age: {age:.2f}ms)")
            
            self.process_message(message)
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except json.JSONDecodeError:
            print(" [!] Error: Invalid JSON message")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            print(f" [!] Error in callback: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def run(self):
        """Main consumer loop."""
        connection = None
        try:
            connection, channel = self.create_connection()
            
            print(f" [*] Starting consumer at {CONSUMER_RATE} messages/second")
            print(' [*] Waiting for messages. To exit press CTRL+C')
            
            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=self.callback
            )
            
            channel.start_consuming()
            
        except KeyboardInterrupt:
            print(" [*] Consumer stopped by user")
        except Exception as e:
            print(f" [!] Unexpected error: {e}")
        finally:
            if connection and not connection.is_closed:
                connection.close()

if __name__ == '__main__':
    consumer = SlowConsumer()
    consumer.run()