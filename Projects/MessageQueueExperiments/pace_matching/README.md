# Pace Matching Experiment

This project demonstrates handling speed mismatches between fast producers and slow consumers using RabbitMQ, implementing back-pressure mechanisms and monitoring.

## Features

1. Fast Producer (1000 msg/sec)
   - Batch publishing
   - Rate limiting
   - Back-pressure handling
   - Publisher confirms

2. Slow Consumer (100 msg/sec)
   - Controlled processing rate
   - Prefetch count management
   - Error handling
   - Message age tracking

3. Monitoring System
   - Queue depth tracking
   - Memory usage monitoring
   - Message rates (in/out)
   - Processing latency
   - Back-pressure events
   - Prometheus metrics

## Prerequisites

1. Python 3.8+
2. RabbitMQ Server
3. pip (Python package manager)

## Setup Instructions

1. Install RabbitMQ Server
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

## Running the Experiment

1. Start the monitoring system:
   ```bash
   python monitor.py
   ```

2. Start the slow consumer:
   ```bash
   python slow_consumer.py
   ```

3. Start the fast producer:
   ```bash
   python fast_producer.py
   ```

4. Monitor metrics at:
   - http://localhost:8000 (Prometheus metrics)
   - http://localhost:15672 (RabbitMQ management interface)

## Back-Pressure Mechanisms

1. Publisher Confirms
   - Ensures message delivery
   - Provides feedback for rate control

2. Queue Size Limits
   - Prevents memory exhaustion
   - Triggers publish rejections

3. Rate Adaptation
   - Reduces producer rate under pressure
   - Maintains minimum throughput

## Testing Scenarios

1. Normal Operation
   - Observe queue depth growth
   - Monitor processing latency

2. Back-Pressure Testing
   - Stop consumer temporarily
   - Watch producer rate adaptation
   - Observe queue limits

3. Recovery Testing
   - Resume consumer
   - Monitor queue drain rate
   - Check message processing order

## Configuration

Key settings in `config.py`:
- Producer rate (messages/second)
- Consumer rate (messages/second)
- Queue size limits
- Monitoring thresholds
- Back-pressure parameters

## Monitoring Metrics

1. Queue Metrics
   - Current depth
   - Input/output rates
   - Message age

2. System Metrics
   - Memory usage
   - Processing latency
   - Back-pressure events

## Troubleshooting

1. High Queue Depth
   - Check consumer health
   - Verify processing rate
   - Look for error patterns

2. High Latency
   - Monitor system resources
   - Check message processing time
   - Verify network conditions

3. Back-Pressure Events
   - Review queue limits
   - Check memory usage
   - Adjust producer rate