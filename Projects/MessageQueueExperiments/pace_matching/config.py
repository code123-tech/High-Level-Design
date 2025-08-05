"""Configuration settings for the Pace Matching system."""

# RabbitMQ connection settings
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'

# Queue settings
QUEUE_NAME = 'pace_matching_queue'
DEAD_LETTER_QUEUE = 'pace_matching_dlq'

# Producer settings
PRODUCER_RATE = 1000  # messages per second
BATCH_SIZE = 50      # messages per batch
MAX_QUEUE_SIZE = 10000  # maximum messages in queue
PUBLISHER_CONFIRMS = True

# Consumer settings
CONSUMER_RATE = 100    # messages per second
PREFETCH_COUNT = 100   # max unacked messages
PROCESSING_TIME = 0.01  # seconds per message (simulated work)

# Monitoring settings
METRICS_PORT = 8000
QUEUE_DEPTH_THRESHOLD = 5000  # alert threshold
MEMORY_USAGE_THRESHOLD = 80   # percentage
LATENCY_THRESHOLD = 1000      # milliseconds

# Back-pressure settings
FLOW_CONTROL_THRESHOLD = 8000  # messages
RATE_REDUCTION_FACTOR = 0.8    # reduce rate by 20% when threshold reached
MIN_PUBLISH_RATE = 100         # minimum messages per second