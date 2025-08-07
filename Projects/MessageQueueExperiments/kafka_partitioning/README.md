# Kafka Partitioning Exercise

This exercise demonstrates various Kafka partitioning strategies and consumer group behaviors.

## Prerequisites

1. Python 3.7+ installed
2. Docker and Docker Compose installed (for running Kafka)
3. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Project Structure

- `config.py`: Configuration settings for Kafka
- `topic_manager.py`: Creates multi-partition topic
- `custom_partitioner.py`: Custom partitioning strategies
- `producer.py`: Message producer with different partitioning strategies
- `consumer.py`: Consumer group demonstration
- `docker-compose.yml`: Docker configuration for Kafka and Zookeeper
- `run_demo.py`: Script to run all components together

## Setting up Kafka with Docker Compose

The project includes a `docker-compose.yml` that sets up:
- Zookeeper (required for Kafka)
- Kafka broker with 4 partitions

To start Kafka:

```bash
# Start Kafka and Zookeeper
docker-compose up -d

# To check if containers are running
docker-compose ps

# To view logs
docker-compose logs -f

# To stop when done
docker-compose down
```

The Kafka broker will be available at `localhost:9092`.

## Running the Exercise

### Option 1: Run All Components Together
```bash
python run_demo.py
```
This will:
1. Create the topic
2. Start consumer group
3. Run producer with different partitioning strategies

### Option 2: Run Components Separately

1. First, create the topic:
```bash
python topic_manager.py
```

2. Start multiple consumers in a group:
```bash
python consumer.py
```

3. In a new terminal, run the producer to test different partitioning strategies:
```bash
python producer.py
```

## Features Demonstrated

1. **Multiple Partitions**: Topic created with 4 partitions

2. **Custom Partitioning Strategies**:
   - Default Partitioner
   - Round Robin Partitioner
   - Key-Based Partitioner

3. **Consumer Groups**:
   - Multiple consumers in the same group
   - Automatic partition rebalancing
   - Message distribution across consumers

4. **Monitoring**:
   - Partition assignment tracking
   - Message routing visualization
   - Consumer group behavior observation

## Expected Output

The exercise will show:
- How messages are distributed across partitions
- How different partitioning strategies affect message distribution
- How consumer groups share the partitions
- What happens during consumer group rebalancing

## Docker Compose Configuration Details

The `docker-compose.yml` includes:

1. **Zookeeper**:
   - Port: 2181
   - Anonymous login enabled
   - Used for Kafka cluster management

2. **Kafka**:
   - Port: 9092
   - Automatically creates topic with 4 partitions
   - Configured for local development
   - Volume mounted for persistence

## Troubleshooting

1. **Kafka Not Available**:
   - Ensure Docker is running
   - Check container status with `docker-compose ps`
   - View logs with `docker-compose logs kafka`

2. **Connection Issues**:
   - Verify Kafka is running on port 9092
   - Check if topic is created using `docker-compose exec kafka kafka-topics.sh --list --bootstrap-server localhost:9092`

## Notes

- The exercise uses colored output for better visualization
- Consumer group behavior can be observed by starting/stopping consumers
- Key-based partitioning ensures messages with the same key go to the same partition
- Docker volumes ensure data persistence between restarts