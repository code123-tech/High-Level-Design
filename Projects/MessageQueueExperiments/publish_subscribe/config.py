"""Configuration settings for the RabbitMQ Pub/Sub system."""

# RabbitMQ connection settings
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'

# Exchange settings
TOPIC_EXCHANGE = 'news_exchange'

# Queue settings
SPORTS_QUEUE = 'sports_queue'
TECH_QUEUE = 'tech_queue'
WEATHER_QUEUE = 'weather_queue'

# Routing patterns
SPORTS_PATTERN = 'sports.#'  # All sports news
TECH_PATTERN = 'tech.*'      # Direct tech categories
WEATHER_PATTERN = 'weather.*' # Direct weather categories