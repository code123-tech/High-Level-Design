# Publish/Subscribe Message Queue System

This project demonstrates a publish/subscribe messaging pattern using RabbitMQ with topic-based routing.

## Prerequisites

1. Python 3.8+
2. RabbitMQ Server
3. pip (Python package manager)

## Project Structure

```
publish_subscribe/
├── config.py           # Configuration settings
├── base_consumer.py    # Base consumer class
├── sports_consumer.py  # Sports news consumer
├── tech_consumer.py    # Technology news consumer
├── weather_consumer.py # Weather updates consumer
├── publisher.py        # News publisher
└── requirements.txt    # Python dependencies
```

## Setup Instructions

1. Install RabbitMQ Server
   - Download and install from [RabbitMQ official website](https://www.rabbitmq.com/download.html)
   - Make sure the RabbitMQ server is running
   - docker command to install rabbitmq:
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
   ```   

2. Create Python Virtual Environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the consumers in separate terminals:
   ```bash
   # Terminal 1
   python sports_consumer.py

   # Terminal 2
   python tech_consumer.py

   # Terminal 3
   python weather_consumer.py
   ```

2. Start the publisher in a new terminal:
   ```bash
   python publisher.py
   ```

## Topic Patterns

- Sports news: `sports.#` (matches sports.football, sports.basketball, etc.)
- Tech news: `tech.*` (matches tech.mobile, tech.ai, etc.)
- Weather updates: `weather.*` (matches weather.london, weather.newyork, etc.)

## Features

1. Topic-based routing using wildcards
2. Multiple independent consumers
3. Message persistence
4. Error handling and recovery
5. Clean shutdown handling

## Testing Scenarios

1. Start all consumers and observe message distribution
2. Stop one consumer and see messages queue up
3. Restart the consumer and see queued messages processed
4. Try different topic patterns and routing keys