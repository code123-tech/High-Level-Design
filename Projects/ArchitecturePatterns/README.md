# Architecture Patterns Demo

This project demonstrates different high availability architecture patterns using Python, FastAPI, and Docker. It includes implementations of:

1. Single Node Architecture
2. Active-Passive Architecture
3. Active-Active Architecture
4. Monitoring and Health Checks
5. Load Testing and Failover Scenarios

## Project Structure

```
ArchitecturePatterns/
├── app/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Data models
│   └── database.py       # Database connections
├── docker/
│   ├── single-node/      # Single node setup
│   ├── active-passive/   # Active-passive setup
│   └── active-active/    # Active-active setup
├── monitoring/
│   ├── prometheus/       # Prometheus configuration
│   └── grafana/          # Grafana dashboards
├── tests/
│   ├── load_tests/       # k6 load tests
│   └── failover_tests/   # Failover scenarios
└── docker-compose.yml    # Main compose file
```

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- kubectl (for Kubernetes deployments)

## Quick Start

1. Clone this repository
2. Navigate to the project directory:
   ```bash
   cd Projects/ArchitecturePatterns
   ```

## Architecture Patterns

### 1. Single Node
This setup demonstrates a basic architecture with one database instance.

#### Running the Single Node Setup
```bash
# Start all services
docker compose -f docker/single-node/docker-compose.yml up -d

# Stop all services
docker compose -f docker/single-node/docker-compose.yml down

# View logs
docker compose -f docker/single-node/docker-compose.yml logs -f

# Rebuild and restart
docker compose -f docker/single-node/docker-compose.yml up --build -d
```

#### Accessing Services
- **FastAPI Application**:
  - Main API: http://localhost:8888
  - API Documentation: http://localhost:8888/docs
  - Health Check: http://localhost:8888/health
  - Metrics: http://localhost:8888/metrics

- **PostgreSQL Database**:
  ```
  Host: localhost
  Port: 5434
  Database: demo
  Username: postgres
  Password: example
  ```

- **Prometheus** (Metrics Collection):
  - Main Interface: http://localhost:9092
  - Targets Page: http://localhost:9092/targets
  - Graph/Query Interface: http://localhost:9092/graph

- **Grafana** (Monitoring Dashboard):
  - URL: http://localhost:3002
  - Login: admin
  - Password: admin

#### Testing the API
```bash
# Create a test item
curl -X POST "http://localhost:8888/items/?name=test_item"

# List all items
curl http://localhost:8888/items/

# Check health
curl http://localhost:8888/health
```

#### Common Issues
1. Port conflicts: If ports are already in use, modify the port mappings in `docker/single-node/docker-compose.yml`
2. Database connection issues: Check if PostgreSQL container is running using `docker ps`
3. Service not starting: Check logs using `docker compose -f docker/single-node/docker-compose.yml logs [service_name]`

### 2. Active-Passive
- Primary-Secondary database setup
- Automatic failover
- Data replication

### 3. Active-Active
- Multiple active nodes
- Load balancing
- Conflict resolution

## Monitoring

- Prometheus metrics
- Grafana dashboards
- Health check endpoints
- Performance monitoring

## Testing

- Load testing with k6
- Failover scenario testing
- Consistency checks
- Performance benchmarks

## Learning Objectives

Each pattern demonstrates:
- Setup and configuration
- Failover mechanisms
- Data consistency
- Performance characteristics
- Monitoring and alerting 