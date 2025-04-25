### Introduction
- A key-value storage system is a kind of NoSQL database system that stores data as collection of `key:value` pairs. Unlike relational DBs, this type of storage are schema-less.
- Examples:
    - `Redis`: In-memory data structure store, used as database, cache and message broker.
    - `DynamoDB`: NoSQL database used by almost all internal services at Amazon.
    - `Cassandra`: Distributed NoSQL database designed to handle large amount of data across many commodity servers.
    - `Memcached`: Distributed memory object caching system.

### Requirements
- `System design requirements` are basically some functional/non-functional contstraints that the system should operate under.
- `Function Requirements:`
    - `PUT Operation:` store a key:value pair in the storage
    - `GET Operation:` retrieve the value for a given key

- `Non-Functional Requirements:`
    - `Storage:` able to store large amount of data (let's assume amount of data not placable on one machine)
    - `Reliable:` There should be no SOPF (Single point of failure), and data should be reliably inserted into the system.
    - `Read Scalable:` should be able to accommodate sudden spike/increase in traffic.
    - `Availability:` should be available with minimal downtime and no SOPF.
    - `Eventual Consistency:` Read, issued right after write operation should not be guaranteed to return the latest value, this can present for a little but non-deterministic time.
    - can consider `Low Latency` and `Fault tolerance` also for this system.

### Simple In Memory Key-Value store
- Consider a key-value store resides on single server, and in memory is straightforward to implement. 
- In this, we have single OS process with in memory dictionary to store the data.
- `Benefits:`
    1. It's easy to implement.
    2. It's fast.
- `Drawbacks:` The main reason of this type of system is not good as they do not meet the non-functional requirements. There are high chances of SOPF in this type of system.
    - `Not reliable:` If server permanently dies, all the data is lost.
    - `Not Available:` If server temporarily dies, data is not accessible
    - `Not Scalable:` If sudden traffic spike occurs, there are high chances of it's crash as we are operating on Single OS process.

- All this problem has one major thing `Single Point of failure (SOPF)` which can be solved by distributing request into N operational points, this fail-over mechanism is called `Distributed system`.

### CAP theorum
- Read about it from [here](../../BasicConcepts/CAP_Theorum.md)

### Data Partitioning
- For Large scale applications, It is not feasible to store data on a single dB server as it will become slow or even worse at the end and storage space can also increase.
- The solution of this problem is `Data Partitioning: partition data into chunks and store them on multiple machines.`
- In this case evenly distribute data on different machines and add an application level logic follows 2 rules:
    1. Evenly distribute data b/w existing machines
    2. In case of machine failure or new machine addition, data should be re-distributed.

- So, this seems easy in theory, but it's little complex in implement it. To handle such kind of situations, a concept called `Consistent Hashing` is used. Read of it from [here](../../BasicConcepts/Consistent_Hashing.md) and [Basic implementation](../ConsistentHashing)

### Data Replication
- To achieve reliability and high availability, we need to get rid of SOPF from the system.
- One of the solution is `Data Replication: To have N copies of same data on N geographically distributed servers.` This will help us in loosing data in case of permanent/temporal machine failures.
- There are various variations of data replication like: `active-passive, active-active etc.`
- `active-active` are complex as they target scalability on write as well read operations.
- `active-passive:` this are ones which mostly focuses on read-heavy systems.
    - Here 1 master handles write operations node and N follower nodes handles all reads.
    - One of most popular implementation of this is `Raft consensus protocol`.

#### Raft consensus Algorithm
- This algorithm says
    - All the writes are handled by master node only. Each and every write command is considered successful if and only if the master node gets acknowledgement from majority of the follower nodes that they have written the data successfully.
    - Reads can be handled by any one of N follower nodes. Meaning we can have dynamic number of followers depending on the stress of system. one quite interesting side effects of replication is that we'll be able to place replicated geographically closer to the clients that issue bunch of read requests, thus decreasing actual latency for them.

- One tradeoff in this protocol is that atleast majority of the nodes should be up and running for giving acknowledgement. for ex: For N nodes, atleast `N/2 + 1` nodes should be up and running for the system to be operational. This is called `quorum`.
- More of raft algorithm can be read from [here1](https://raft.github.io/), and [here2](https://youtu.be/aE2UPg3Ckck).


### Consistency Guarantees
- Before this, watch [different types of conssistency video](https://youtu.be/Fm8iUFM2iWU). So, above replication techniques gives us high availability, reliability, and other benefits, but it can cause `potential inconsistency` between replicas.
The problem is of `Eventual Consistency`. 
As for example a write request is sent to master node, and master node gets confirmation from majority of the followers. 
Now, suppose read request comes and it is redirected to one of the follower node where data is not replicated yet, this may cause incosistency problem but for a system with high availability, this is acceptable for a small fraction of time.


