# Architecture Patterns Demo

This project demonstrates different high availability architecture patterns using Python, FastAPI, and Docker.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Quick Start](#quick-start)
5. [Architecture Patterns](#architecture-patterns)
   - [Single Node](#1-single-node)
   - [Active-Passive](#2-active-passive)
   - [Active-Active](#3-active-active)
6. [Monitoring Setup](#monitoring-setup)
   - [Prometheus Configuration](#prometheus-monitoringprometheus)
   - [Grafana Dashboards](#grafana-monitoringgrafana)
   - [Using Monitoring Tools](#how-to-use-monitoring)
6. [Testing](#testing)
   - [Load Testing](#load-testing)
   - [Monitoring Test Results](#monitoring-test-results)
   - [Failover Testing](#failover-testing)
7. [Learning Objectives](#learning-objectives)
8. [References](#references)
   - [Architecture Patterns (Theory)](#architecture-patterns-theory)
   - [Monitoring & Testing](#monitoring--testing)
   - [Tools Used](#tools-used)
   - [Further Reading](#further-reading)

## Project Overview

This project includes implementations of:
1. Single Node Architecture
2. Active-Passive Architecture
3. Active-Active Architecture
4. Monitoring and Health Checks
5. Load Testing and Failover Scenarios

## Project Structure

```
ArchitecturePatterns/
├── app/
│   ├── main.py           # FastAPI 
│   ├── models.py         # Data models
│   └── database.py       # Database 
├── docker/
│   ├── single-node/      # Single node
│   ├── active-passive/   # Active-passive
│   └── active-active/    # Active-active 
├── monitoring/
│   ├── prometheus/       # Prometheus 
│   └── grafana/          # Grafana 
├── tests/
│   ├── load_tests/       # k6 load tests
│   └── failover_tests/   # Failover 
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

## Monitoring Setup

The `/monitoring` directory contains configurations for observability and alerting:

### Prometheus (`/monitoring/prometheus/`)
1. **Alert Rules** (`rules/alerts.yml`):
   - High Request Latency (>500ms)
   - High Error Rate (>10%)
   - API Down Detection
   - Database Connection Issues
   - System Alerts (CPU, Memory, Disk)

2. **Recording Rules** (`rules/recording.yml`):
   - API Metrics (request rate, error rate, response times)
   - Node Metrics (CPU, memory, disk usage)
   - Pre-computed metrics for faster querying

### Grafana (`/monitoring/grafana/`)
- API Dashboard with:
  - Request Rate Visualization
  - Response Time Metrics
  - Error Rate Tracking
  - System Resource Usage

### How to Use Monitoring

1. **View Metrics**:
   - Prometheus UI: http://localhost:9092
   - Grafana Dashboards: http://localhost:3002 (admin/admin)

2. **Check Alerts**:
   - Active Alerts: http://localhost:9092/alerts
   - Alert History: Grafana Alert Tab

3. **Common Queries**:
   ```
   # Request Rate
   api:request_rate:5m

   # Error Rate
   api:error_rate:5m

   # System Health
   node:cpu_usage:5m
   node:memory_usage:5m
   ```

4. **Testing Alerts**:
   - Run load tests to trigger performance alerts
   - Use failover tests to trigger availability alerts


## Testing

### Load Testing
Located in `/tests/load_tests/`:
- Uses Locust for load testing
- Simulates multiple users accessing the API
- Measures response times and error rates
- Helps identify performance bottlenecks

To run load tests:
```bash
# Start Locust web interface
locust -f tests/load_tests/locustfile.py --host http://localhost:8888

# Or run headless mode with specific parameters
locust -f tests/load_tests/locustfile.py --host http://localhost:8888 --headless -u 10 -r 2 --run-time 30s
```

Parameters explained:
- `-u 10`: Simulate 10 users
- `-r 2`: Spawn 2 users per second
- `--run-time 30s`: Run for 30 seconds

### Monitoring Test Results

#### Grafana Dashboard Setup
1. Access Grafana at http://localhost:3002 (login: admin/admin)
2. Go to "+" icon > Import
3. Upload the dashboard JSON file from:
   ```
   monitoring/grafana/api_dashboard.json
   ```
4. Select "Prometheus" as the data source
5. Click "Import"

The dashboard shows:
- API Request Rate (requests per second)
- Response Times (average and 95th percentile)
- Auto-refreshes every 5 seconds
- Shows last 15 minutes of data

### Failover Testing
Located in `/tests/failover_tests/`:
- Tests system resilience during database failures
- Simulates database container stops/starts
- Measures system recovery time
- Verifies data consistency

To run failover tests:
```bash
# Run the database failover test
python -m tests.failover_tests.database_failover
```

What the test does:
1. Creates test data in database
2. Verifies initial system health
3. Simulates database failure
4. Checks API behavior during outage
5. Restores database
6. Measures recovery time
7. Reports test results

Expected output:
```
INFO: Starting failover test...
INFO: Stopping database container...
INFO: API health check during failure: Failed as expected
INFO: Starting database container...
INFO: System recovered in X.XX seconds
INFO: Failover test succeeded
```

## Learning Objectives

Each pattern demonstrates:
- Setup and configuration
- Failover mechanisms
- Data consistency
- Performance characteristics
- Monitoring and alerting 

## References

### Architecture Patterns (Theory)
- [High Availability Database Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/category/availability) - Microsoft Azure Architecture Guide
- [Failover Strategies](https://aws.amazon.com/blogs/architecture/disaster-recovery-dr-architecture-on-aws-part-i-strategies-for-recovery-in-the-cloud/) - AWS Architecture Blog

### Monitoring & Testing
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboard Guidelines](https://grafana.com/docs/grafana/latest/best-practices/dashboard-management-best-practices/)
- [Load Testing with Locust](https://docs.locust.io/en/stable/what-is-locust.html)

### Tools Used
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [PostgreSQL High Availability](https://www.postgresql.org/docs/current/high-availability.html)

### Further Reading
- "Building Microservices" by Sam Newman
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Site Reliability Engineering" by Google 