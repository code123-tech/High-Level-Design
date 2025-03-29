### *Introduction*
- *Definition:* Consistent Hashing is a hashing technique widely used in an envrionment which is dynamic and where distributed system scales up and down frequently. 

- *Advantage:* 
    - In normal Hashing, the domain size should be fixed, otherwise the hash table needs to be rehashed. This is not feasible in a distributed system where servers are added or removed frequently. That's where Consistent Hashing comes into play.
    - Consistent Hashing allows for minimal rehashing when servers are added or removed.

- *Disadvantage:*
    - It can lead to data skewness, where some servers have more data than others.
        - To mitigiage this, we can use *Virtual Nodes* which are replicas of physical nodes, allowing for more even distribution of data.
    - It can be complex to implement and maintain compared to traditional hashing.
    - Require huge memory space to store the hash values.
    - finding immediate right node by iterating is time consuming which is `O(hash_space)`

- *USe cases:*
    - *Load Balancer:* Distributing incoming requests across multiple servers.
    - *Database Sharding:* Partitioning data across multiple database servers, ensuring even distribution.
    - *Caching:* Storing frequently accessed data in cache servers.
    - *Distributed File Systems:* Storing files across multiple servers for redundancy and performance.

### *How Consistent Hashing Works*
- *Basic Idea:*
    - Consistent hashing keeps the hash space huge and constant, somehwere in range of `[0, 2^128-1]`.
    - Both the servers (nodes) and incoming key (data/request) are hashed to a value in this range itself, and kept in a circular ring.
    - Instead of traditional hashing, where the key is hashed to a fixed number of buckets (It can lead to collision problem), to avoid that In consistent hashing -> the key is mapped to the server which is at immediate right or current hashed valued location.
    - `Consitent Hashing on the average required 1/N keys to be remapped when a server is added or removed, where N is the number of servers.`  

- *Hash function in Consistent Hashing:*
    - Typically hash function is implemented by `SHA-256` or `MD5` which further followed by `mod space_size`. 
    - `space_size:` size of the entire hash space.

- *Adding a node/server`
    - When a new server/node is added, it's hash value/position is calculated to be placed in the hash ring.
    - Populate this new node with the data which is between the previous node (towards left) and current hashed location.
    - This way, only the data between the previous node (towards left) and current hashed location needs to be remapped.

- *Removing a node/server*
    - When a server is removed, the data which is between the previous node (towards left) and current hashed location needs to be remapped to the next node.
    - This way, only the data between the previous node (towards left) and current hashed location needs to be remapped.

### *References*
- `Code reference:` [reference](https://github.com/arpitbbhayani/consistent-hashing/blob/master/consistent-hashing.ipynb)
- `Blogs:` [blog](https://arpitbhayani.me/blogs/consistent-hashing/)
- `Videos:` [video](https://youtu.be/jqUNbqfsnuw?list=PL6W8uoQQ2c63W58rpNFDwdrBnq5G3EfT7)
