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
