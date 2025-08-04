"""Base consumer class for all topic consumers."""

import pika
import json
from abc import ABC, abstractmethod
from config import *

class BaseConsumer(ABC):
    def __init__(self, queue_name, routing_pattern):
        self.queue_name = queue_name
        self.routing_pattern = routing_pattern
        
    def create_connection(self):
        """Create a connection to RabbitMQ server."""
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)
    
    def setup_queue(self, channel):
        """Setup exchange, queue and binding."""
        # Declare the exchange
        channel.exchange_declare(
            exchange=TOPIC_EXCHANGE,
            exchange_type='topic',
            durable=True
        )
        
        # Declare the queue
        channel.queue_declare(
            queue=self.queue_name,
            durable=True
        )
        
        # Bind queue to exchange with routing pattern
        channel.queue_bind(
            exchange=TOPIC_EXCHANGE,
            queue=self.queue_name,
            routing_key=self.routing_pattern
        )
    
    @abstractmethod
    def process_message(self, message_data):
        """Process the received message - to be implemented by specific consumers."""
        pass
    
    def callback(self, ch, method, properties, body):
        """Callback function for handling received messages."""
        try:
            message = json.loads(body)
            print(f"\nReceived message on {self.queue_name}")
            print(f"Routing Key: {method.routing_key}")
            self.process_message(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except json.JSONDecodeError:
            print(" [!] Error: Invalid JSON message")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            print(f" [!] Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start_consuming(self):
        """Start consuming messages."""
        try:
            connection = self.create_connection()
            channel = connection.channel()
            
            self.setup_queue(channel)
            
            # Set QoS
            channel.basic_qos(prefetch_count=1)
            
            # Start consuming
            channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.callback
            )
            
            print(f" [*] {self.queue_name} waiting for messages. To exit press CTRL+C")
            channel.start_consuming()
            
        except KeyboardInterrupt:
            print(f"\n [*] {self.queue_name} consumer stopped by user")
        except Exception as e:
            print(f" [!] Unexpected error: {e}")
        finally:
            if connection and not connection.is_closed:
                connection.close()