"""Fast producer generating 1000 messages per second with back-pressure handling."""

import pika
import json
import time
import threading
from datetime import datetime
from monitor import monitor
from config import *

class FastProducer:
    def __init__(self):
        self.current_rate = PRODUCER_RATE
        self.confirm_tokens = threading.Semaphore(MAX_QUEUE_SIZE)
        self.message_count = 0
        self.should_stop = False
        
    def create_connection(self):
        """Create a connection to RabbitMQ with publisher confirms."""
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # Enable publisher confirms
        if PUBLISHER_CONFIRMS:
            channel.confirm_delivery()
        
        # Declare queue with max length limit
        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True,
            arguments={
                'x-max-length': MAX_QUEUE_SIZE,
                'x-overflow': 'reject-publish'
            }
        )
        
        return connection, channel
    
    def publish_message_batch(self, channel):
        """Publish a batch of messages."""
        try:
            batch_size = min(BATCH_SIZE, int(self.current_rate / 10))  # Adjust batch size based on rate
            messages_published = 0
            
            for _ in range(batch_size):
                # Wait for confirm token
                self.confirm_tokens.acquire()
                
                message = {
                    'id': self.message_count,
                    'content': f'Message {self.message_count}',
                    'timestamp': datetime.now().isoformat()
                }
                
                try:
                    # Publish with mandatory flag to get returns on routing failures
                    channel.basic_publish(
                        exchange='',
                        routing_key=QUEUE_NAME,
                        body=json.dumps(message),
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # Make message persistent
                            timestamp=int(time.time())
                        ),
                        mandatory=True
                    )
                    
                    # For each message, wait for confirmation
                    if PUBLISHER_CONFIRMS:
                        if channel.wait_for_confirms(timeout=0.1):
                            messages_published += 1
                            monitor.increment_message_in()
                            self.message_count += 1
                        else:
                            print(" [!] Message was not confirmed")
                            self._apply_back_pressure()
                    else:
                        messages_published += 1
                        monitor.increment_message_in()
                        self.message_count += 1
                    
                    # Release token since we got confirmation
                    self.confirm_tokens.release()
                    
                except pika.exceptions.UnroutableError:
                    print(" [!] Message was returned - queue might be full")
                    self._apply_back_pressure()
                    self.confirm_tokens.release()
                    
            if messages_published > 0 and messages_published < batch_size:
                print(f" [!] Only published {messages_published}/{batch_size} messages")
                self._apply_back_pressure()
                
        except Exception as e:
            print(f" [!] Error publishing batch: {e}")
            self._apply_back_pressure()
    
    def _apply_back_pressure(self):
        """Reduce publishing rate when back pressure is detected."""
        self.current_rate = max(
            MIN_PUBLISH_RATE,
            int(self.current_rate * RATE_REDUCTION_FACTOR)
        )
        print(f" [*] Applying back pressure - new rate: {self.current_rate} msg/sec")
    
    def run(self):
        """Main producer loop."""
        connection = None
        try:
            connection, channel = self.create_connection()
            
            print(f" [*] Starting producer at {self.current_rate} messages/second")
            
            while not self.should_stop:
                batch_start = time.time()
                
                # Publish batch
                self.publish_message_batch(channel)
                
                # Calculate sleep time to maintain rate
                elapsed = time.time() - batch_start
                sleep_time = max(0, (BATCH_SIZE / self.current_rate) - elapsed)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            print(" [*] Producer stopped by user")
        except Exception as e:
            print(f" [!] Unexpected error: {e}")
        finally:
            if connection and not connection.is_closed:
                connection.close()

if __name__ == '__main__':
    producer = FastProducer()
    producer.run()