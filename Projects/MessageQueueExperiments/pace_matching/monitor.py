"""Simple monitoring system for the Pace Matching experiment."""

import time
import threading
import pika
from config import *

class QueueMonitor:
    def __init__(self):
        self.message_rate_in = 0
        self.message_rate_out = 0
        self.processing_latency = 0
        self.back_pressure_events = 0
        
        # Start monitoring thread
        self.should_stop = False
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _get_queue_metrics(self):
        """Get current queue metrics from RabbitMQ."""
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
                )
            )
            channel = connection.channel()
            
            # Get queue information
            queue_info = channel.queue_declare(
                queue=QUEUE_NAME,
                passive=True  # Don't create queue, just get info
            )
            
            connection.close()
            return queue_info.method.message_count
            
        except Exception as e:
            print(f"Error getting queue metrics: {e}")
            return 0
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        last_in_count = 0
        last_out_count = 0
        
        while not self.should_stop:
            try:
                # Get current queue depth
                queue_depth = self._get_queue_metrics()
                
                # Calculate rates
                current_in = self.message_rate_in
                current_out = self.message_rate_out
                
                in_rate = current_in - last_in_count
                out_rate = current_out - last_out_count
                
                last_in_count = current_in
                last_out_count = current_out
                
                # Print monitoring information
                print("\n=== Monitoring Statistics ===")
                print(f"Queue Depth: {queue_depth} messages")
                print(f"Input Rate: {in_rate} msg/sec")
                print(f"Output Rate: {out_rate} msg/sec")
                print(f"Processing Latency: {self.processing_latency:.2f} ms")
                print(f"Back Pressure Events: {self.back_pressure_events}")
                print("==========================\n")
                
                # Check thresholds
                if queue_depth > QUEUE_DEPTH_THRESHOLD:
                    print(f"WARNING: Queue depth ({queue_depth}) exceeds threshold ({QUEUE_DEPTH_THRESHOLD})")
                    self.back_pressure_events += 1
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    def increment_message_in(self):
        """Increment the messages-in counter."""
        self.message_rate_in += 1
    
    def increment_message_out(self):
        """Increment the messages-out counter."""
        self.message_rate_out += 1
    
    def record_latency(self, latency_ms):
        """Record message processing latency."""
        self.processing_latency = latency_ms
    
    def stop(self):
        """Stop the monitoring thread."""
        self.should_stop = True
        self.monitor_thread.join()

# Global monitor instance
monitor = QueueMonitor()

if __name__ == '__main__':
    print("Starting Queue Monitor")
    print("Press Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
        print("\nMonitor stopped")