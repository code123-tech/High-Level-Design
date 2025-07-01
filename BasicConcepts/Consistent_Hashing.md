## Table of Contents
1. [Introduction](#introduction)
2. [How Consistent Hashing Works](#how-consistent-hashing-works)
3. [References](#references)

## Introduction
- *Definition:* Consistent Hashing is a hashing technique widely used in an environment where distributed systems scale up and down frequently. 

- *Advantage:* 
    - In normal Hashing, the domain size should be fixed, otherwise the hash table needs to be rehashed. This is not feasible in a distributed system where servers are added or removed frequently. That's where Consistent Hashing comes into play.
    - Consistent Hashing allows for minimal rehashing when servers are added or removed.

- *Disadvantage:*
    - It can lead to data skewness, where some servers have more data than others.
        - To mitigate this, we can use *virtual nodes (v-nodes)*—multiple hash-points per physical node—to smooth out the distribution.
    - It can be complex to implement and maintain compared to traditional hashing.
    - Requires extra memory to keep the routing table (≈ N × V entries, where V is the number of virtual nodes).
    - Lookup for the next node is `O(log N)` via binary search on the sorted ring (N = total virtual nodes).

- *Use cases:*
    - *Load Balancer:* Distributing incoming requests across multiple servers.
    - *Database Sharding:* Partitioning data across multiple database servers, ensuring even distribution.
    - *Caching:* Storing frequently accessed data in cache servers.
    - *Distributed File Systems:* Storing files across multiple servers for redundancy and performance.

## How Consistent Hashing Works
- *Basic Idea:*
    - Consistent hashing keeps the hash space fixed—commonly 2³², 2⁶⁴ or 2¹²⁸—so node joins/leaves do not trigger full re-hash.
    - Both the servers (nodes) and incoming key (data/request) are hashed to a value in this range itself, and kept in a circular ring.
    - Instead of hashing into a fixed number of buckets, the key is mapped to the first server clockwise from its hashed-value location, greatly reducing data movement on membership change.
    - `Consistent hashing, on average, remaps only 1⁄N keys when a server is added or removed (N = #physical servers).`  

- *Hash function in Consistent Hashing:*
    - Typically hash function is implemented by `SHA-256` or `MD5` which further followed by `mod space_size`. 
    - `space_size:` size of the entire hash space.

- *Adding a node/server*
    - When a new server/node is added, it's hash value/position is calculated to be placed in the hash ring.
    - Populate this new node with the data which is between the previous node (towards left) and current hashed location.
    - This way, only the data between the previous node (towards left) and current hashed location needs to be remapped.

- *Removing a node/server*
    - When a server is removed, the data which is between the previous node (towards left) and current hashed location needs to be remapped to the next node.
    - This way, only the data between the previous node (towards left) and current hashed location needs to be remapped.

## References
- `Code reference:` [reference](https://github.com/arpitbbhayani/consistent-hashing/blob/master/consistent-hashing.ipynb)
- `Blogs:` [blog](https://arpitbhayani.me/blogs/consistent-hashing/)
- `Videos:` [video](https://youtu.be/jqUNbqfsnuw?list=PL6W8uoQQ2c63W58rpNFDwdrBnq5G3EfT7)
