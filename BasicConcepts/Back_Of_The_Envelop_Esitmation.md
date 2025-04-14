### Back of Envelop Introdcution
- When designing a large scale system, we need to estimate:
    - How many servers needed?
    - Storage capacity
    - cache size
    - Load Balancers count
    - Content delivery network (CDN) servers etc.
- BoE esitmation helps in making these rough estimates, and drive our decision for system design and selecting components.
- `Key consideration:`
    - Do not spend much time on this (maximum 10 minutes)
    - Do not Aim for high accuracy (take rough esitmation)
    - Use known values which are easy to compute during discussion (use below cheat sheet)

### Cheat Sheet for doing calculation/estimation
| Number of zeros |  Traffic     | Storage             |
| ---             | ---          | ---                 |
| 3 = 10^3        | Thousand     | KB (KiloBytes)      |
| 6 = 10^6        | Million      | MB (MegaBytes)      |
| 9 = 10^9        | Billion      | GB (GigaBytes)      |
| 12 = 10^12      | Trillion     | TB (TeraBytes)      |
| 15 = 10^15      | Quadrillions | PB (PetaBytes)      |

- Keep values in terms of three zeros to make calculation easy.

- Consider below Memory Reference values:
    ```
    Char size: 2 bytes
    Long/Double size: 8 bytes
    Image Avg size: 300 KB
    ```

- Generally compute following:
    - Number of servers needed for the system
    - Cache/RAM size
    - Storage capacity
    - TradeOffs (CAP theorum)

- Mathematical approach for estimation:
    - `Formula: X(users) * Y(data per user) = Z(total data)`
    - Example:
        ```
        5 million (users), each storing 2 KB of data
        so, total = 5 Million * 2 KB = 10 GB
        ```

### BoE Estimation for Facebook's System design
1. `Traffic/User Estimation`
```md
Suppose total Users = 1 Billion 
Daily Active Users (DAU) = 25% of 1 Billion = 250 Million

Each user doing two types of query daily:
    - READ Query   =  5
    - WRITE Query  =  2

So, total queries = 250 Million * 7 = 1750 Million queries per day
Now, to calculate per second request, let's assume in a day = 100000 seconds

`per second request = 1750 Million / 100000 = around 18K queries per second`
```

2. `Storage Estimation`
```md
Assume, each user doing 2 posts per day (2 write query per day from previous estimation)
Assume, each post has 250 characters 
and 10% of DAU are uploading 1 Image also in their post.

So, for 250 characters 
    - 1 character size = 2 bytes
    - 250 characters = 2 * 250 = 500 bytes
For 1 Image = 300 KB

For characters:
    - each user doing 2 posts, per post size = 500 bytes
    - So, per user post size = 2 * 500 = 1 KB
    - So, for DAU = 250 Million
    - `total size for posts = 250 Million * 1 KB = 250 GB`

For Images:
    - 10% of 250 Million = 25 Million users doing 1 image upload in their post.
    - 1 Image size = 300 KB
    - `so, total size for images = 25 Million * 300 KB = 7.5 TB`

So, `total size = 250 GB + 7.5 TB = 7.75 TB = around 8 TB`

- 8 TB of storage needed daily.
- Suppose system needs to be run for 5 years
- `Calculation of storage for 5 years:`
    - daily storage = 8 TB
    - yearly storage = 8 TB * 365 = 2920 TB
    - `5 years storage = 2920 TB * 5 = 14600 TB = 14.6 PB = 15 PB`
```

3. `RAM Esitmation`
```md
Assumption: each user's last 5 posts are cached in RAM
From previous calculation: 
    - per post size = 500 bytes

Total cache per user
    - 5 posts * 500 bytes = 2500 bytes = 2.5 KB = 3 KB

For 250 Million Daily Active users
    - `total cache = 250 Million * 3 KB = 750 GB`

- If 1 Machine can hold 75GB of RAM
    - `total machines needed = 750 GB / 75 GB = 10 Machines`
```

4. `Server estimation`
```md
Latency per request = 500 milliSecond
It means, in 1 second can serve 2 request.

Suppose, 1 server has 50 Threads, so it will be able to serve 100 requests per second.

`total servers = 18K/100 = 180 servers`
```

5. `TradeOffs (CAP theorum)`
- For Facebook:
    - Partition tolerance is essential as data is distibuted
    - Availability is also essential as users need to access data anytime.
    - Consistency is not that important as user can see stale data -> Eventual consistency.
