# Basic Point-to-Point Queue System

This project demonstrates a basic implementation of a point-to-point messaging system using RabbitMQ.

## Prerequisites

1. Python 3.8+
2. RabbitMQ Server
3. pip (Python package manager)

## Setup Instructions

1. Install RabbitMQ Server
   - Download and install from [RabbitMQ official website](https://www.rabbitmq.com/download.html)
   - Make sure the RabbitMQ server is running

2. Create Python Virtual Environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
basic_point_to_point/
├── requirements.txt
├── README.md
├── producer.py
├── consumer.py
└── config.py
```

## Running the Application

1. Start the consumer:
   ```bash
   python consumer.py
   ```

2. In a new terminal, start the producer:
   ```bash
   python producer.py
   ```

## Components

- `producer.py`: Sends messages to the queue
- `consumer.py`: Receives and processes messages from the queue
- `config.py`: Contains configuration settings

## Learning Objectives

1. Understanding basic message queue operations
2. Implementing producer-consumer pattern
3. Handling message acknowledgments
4. Basic error handling and recovery