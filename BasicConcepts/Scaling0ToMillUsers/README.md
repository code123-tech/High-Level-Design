# Scaling from 0 to Millions of Users

Welcome to the **Scaling Journey** guide. This article walks through the basic implementations/demos of scaling an application from 0 to million users.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Scaling Journey](#scaling-journey)
   * 3.1. Single-Server 💻
   * 3.2. Split App & DB 🗄️
   * 3.3. Load Balancing ⚖️
   * 3.4. Database Replication 📚
   * 3.5. Caching 🔥
   * 3.6. Content Delivery Network 🌐
   * 3.7. Multi-Data-Center 🏢🏢
   * 3.8. Messaging Queue 📩
   * 3.9. Database Sharding 🗂️
4. [Implementation Examples](#implementation-examples)
5. [Performance Metrics](#performance-metrics)
6. [Common Pitfalls](#common-pitfalls)
7. [Further Reading](#further-reading)
8. [Theory](#theory)

---

## Overview
Scaling isn't a single action—it's a sequence of incremental changes made in response to real bottlenecks.  This guide documents those stages, explains **why** each step is taken, highlights **trade-offs**, and provides **code/configuration** samples so you can reproduce the architecture in your own environment.

## Prerequisites
* Basic understanding of the HTTP request/response lifecycle
* Familiarity with relational databases and SQL
* Comfort working with Docker and the command line

If you are new to these topics, consider reading the introductory articles in the `BasicConcepts` folder first.

## Scaling Journey
Each stage below links to an `implementations/<stage>/` folder containing Terraform, Docker Compose or Kubernetes manifests plus minimal application code you can run locally.

| Stage | Users | Primary Bottleneck | Key Solution |
|-------|-------|--------------------|--------------|
| 1️⃣ **Single-Server** | 1 – 1k | Everything on one box | N/A |
| 2️⃣ **Split App & DB** | 1k – 10k | Resource contention | Separate tiers |
| 3️⃣ **Load Balancing** | 10k – 100k | CPU on single app | Horizontal app scaling |
| … | … | … | … |

*(Full details to follow as we build out each stage.)*

## Implementation Examples
The `implementations/` directory will include:
* **Docker Compose** stacks for local experimentation
* **Terraform** modules for cloud deployment
* **Load-testing scripts** (k6, Locust) to reproduce bottlenecks

## Performance Metrics
For every stage we will capture baseline vs optimised numbers:
* **P50/P95 latency**
* **Throughput (req/s)**
* **Infrastructure cost estimate**

## Common Pitfalls
1. **Scaling prematurely** – optimise for *right now*, not hypothetical future load.
2. **Ignoring observability** – you can't fix what you can't see.
3. **Single points of failure** – each stage should reduce SPOFs.

## Further Reading
* "Designing Data-Intensive Applications" – Martin Kleppmann
* "Web Scalability for Startup Engineers" – Artur Ejsmont
* Google SRE books

## Theory

### *Steps for Scaling from 0 to Millions of Users*
- This guide starts from very basic service example step and scales it to millions of users.

1. *Single server:*
    - Basic setup with a single server for the application, database and client.
    - Suitable for initial stage with zero users.

2. *Application and Database layer:*
    - Introduces a separate layer for the application server, handling business logic.
    - DB server handles data storage and retrieval.
    - Enables independent scaling of both application and database.

3. *Load balancing and multiple application servers:*
    - Introduces load balancer to distribute incoming traffic across multiple application servers.
    - Load balancer provides security and privacy.
    - Ensures efficient handling of increased traffic by distributing workload.

4. *Database replication:*
    - Implements master-slave configuration for the database.
    - Master db handles write operations, while slave db handles read operations.
    - Improves performance and provides redundancy in case of db failure.

5. *Caching:*
    - Utilizing a caching layer to store frequently accessed data in memory.
    - Application server checks the cache first before accessing the database.
    - Reduces db loads and improves response time for users.
    - Uses time-to-live (TTL) to manage cached data expiry.

6. *Content Delievery Network (CDN):*
    - Uses a distributed network of cache static content closer to users.
    - Reduces latency and improves website performance worldwide.
    - Handles requests for static content like images, videos, and JS files.
    - In case of cache miss, CDN first ask neighbour CDN for data then from origin DB.

7. *Multiple Data Centers:*
    - Distributes the application and db across multiple data centers.
    - Reduces load on individual data centers and improves reliability.
    - Enables geographically distributed users to access the service efficiently and with minimal latency.
    - Load balancer distributes requests to different data centers based on user location.

8. *Messaging Queue:*
    - Uses messaging queue to handle asynchronous tasks like sending notification or emails.
    - Decouples tasks from the main application flow.
    - Improves performance and reliability by handling high-volume tasks efficiently.
    - Utilizes message brokers like Kafka, RabbitMQ, or SQS.

9. *Database Scaling:*
    - *Vertical Scaling:* Increases the resources of the existing server (CPU, RAM, Storage). This has a limitation and eventually reaches ceiling.
    - *Horizontal Scaling / Data Sharding:* Adds more servers to the existing setup. This is more scalable and can handle increased load.
        - Splits data across multiple databases or tables based on a specific key.
        - can be implemented through vertical sharding (splitting columns) or horizontal sharding (splitting rows). 