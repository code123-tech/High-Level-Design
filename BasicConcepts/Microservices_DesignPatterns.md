### Monolithic Architecture
- Monolithic architecture is a traditional unified model for designing software where the application is built as a single unit.
- *Advantages:*
    - *Simplicity:* Easier to develop, test and deploy.
    - *ACID Transactions:* Easy to maintain ACID transactions as single database is being used here
    - *Performance:* Faster communication between components as they are in the same unit.
    - *DB Join queries:* Easy to perform join queries as all data is in the same database.
- *Disadvantages:*
    - *Tight Coupling:*
        - Changing one line/Fixing one issue can impact other components.
        - Need to test/deploy entire application even for one small change.
    - *Difficult to Scale:*
        - If one component needs scaling, entire application needs to be scaled
    - *Expensive deployments and rollbacks*
        - Entire application needs to be deployed/rolled back even for small changes.
    - *Large codebase:*
        - Everything in a single application
        - codebase grows large over time
        - Difficult to make changes, understand impact

### Why Microservice Architecture?
- To overcome disadvantages of Monolithic architecture.
- Split Large application into small services where each service is responsible for a specific task.

### Advantages of Microservices
- Loose coupling between services
- No Scalability issues
- Idependent test/deployment of services
- Better seperation of concerns
- Faster deployments/release cycles

### Disadvantages of Microservices
- Decomposition of services is difficult/challenging
- Inter service communication is complex
    - Monitoring calls across services
    - Handling errors
- Distributed transaction management is difficult to maintain
    - Across multiple databases

### Microservices design phases
1. Decomposition Pattern
2. Database patterns
3. Communication patterns
4. Integration patterns
5. Deployments patterns
6. Cross cutting concerns like logging, monitoring, security etc.

### Decomposition Pattern
- By Business Capability
    - Split service based on functions like order mgmt, Inventory mgmt etc.
- By subDomain (Domain Driven Design)
    - split large domains into multiple services Eg: Splitting Payment Domain


### Strangler Pattern
- *Purpose:* Gradually refactoring a monolithic application into microservices.
- *How it works:*
    - A `controller` is introduced to handle requests.
    - Initially, controller forwards all the traffic to monolithic application.
    - Gradually, specific functionalities are moved to microservices, and traffic is routed to those services.
    - As more functionalities are added, the monolithic application is gradually "strangled" and replaced by microservices.
- *Advantages:*
    - No disrutpion to existing services.
    - Gradual migration to microservices.
- *DisAdvantages:*
    - Complex to manage both monolithic and microservices at the same time.
    - Requires careful planning and coordination.
- *Example:* Imagine a monolithic ecommerce service being gradually replaced by microservices for order mgmt, inventory mgmt, payment processing etc.

### Data Management in microservices
- *Two approaches:*
    - *Database per service:* Each service has its own database, promoting autonomy and isolation.
    - *Shared Database:* All services share a common database, simplifying data management but increasing coupling.
- *Why DB per service is preferred:*
    - *Scalability:* Allows for independent scaling of individual services without impacting others.
    - *Isolation:* Changes in one service's database do not affect others.
    - *Technology flexibility:* Each service can choose the database technology that best suits its needs.
- *Advantages of shared database:*
    - JOIN Query
    - Transaction property (ACID)
- *Drawbacks of shared database:*
    - *Performance bottlenecks:* Increased contention and performance issues as more services access the same database.
    - *Complexity:* Managing dependencies and ensuring consistency across services becomes challenging.
    - *Limited Scalability:* Scaling the entire database is necessary, even if only one service needs more resources.

### SAGA Pattern
- *Puropose:* Managing distributed transactions across multiple databases, ensuring consistency even if some operation fails.
- *How it works:*
    - A sequence of local transactions is executed within each participating microservice.
    - Each transaction updates the DB and publishes an event.
    - Subsequent transaction listens to this event and continue the process.
    - In case of failures, compensation events are published to undo completed transaction and maintain consistency.

- *Types of SAGA:*
    - *Choreography:* Each service manages its own transactions and listens to events from other services.
    - *Orchestration:* A centralized orchestrator manages the transaction flow, handles the compensation logic and ensures consistency.

- *Example:*
    - An order processing SAGA involving services for order creation, inventory management, and payment processing.
    - If the payment service fails, compensation events are triggerred to cancel the order and update the inventory.

- *Advantages:*
    - Guarantees data consistency across services/distributed transactions.
    - Provides mechanism for handling failures/rollbacks.
    - Allows for flexibility in service interactions.

- *Disadvantages:*
    - Increased complexity compared to local transactions.
    - Requires careful design and implementation to ensure consistency.
- *Interview question:*
    - Explain how you would handle a transaction involving transferring money between two users in a microservice architecture.

### CQRS (Command Query Responsibility Segregation)
- *Purpose:* Seperating read (query) operations from write (command) operations for better perforamce and scalability.

- *How it works:*
    - The system maintains seperate models for read and write operations.
    - write operations are performed through commands, updating write models.
    - read operations are performed through queries, fetching data from read models which can be optimized for fast retrievel.

- *Advantages:*
    - *Performance Improvement:* Optimized read models for faster query operations.
    - *Scalability:* Seperate read and write models allow for independent scaling.
    - *Flexibility:* Allows for different models to be used for read and write operations.

- *Example:*
    - A blog application where write operations are performed on a relational DB, while read operations access a denormalized view optimized for fast search.

- *Challenges:*
    - Maintaining consistency between read and write models.
    - Ensuring read model is upto date with change in write model.