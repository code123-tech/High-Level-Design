"""Configuration settings for the RabbitMQ connection."""

# RabbitMQ connection settings
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'

# Queue settings
QUEUE_NAME = 'task_queue'

# Message settings
MESSAGE_PROPERTIES = {
    'delivery_mode': 2,  # Make messages persistent
}