### Introduction
- URL shortening service helps to map a large URL to shorter version of the URL. Now, 
  this shorter URL can be used to access the original URL.

### Phases
1. *Requirement Analysis:*
    - What characters can be included in the shorter URL/code?
        - characters: `a-z`, `A-Z`, `0-9`
        - Total characters: `62`

    - What can be the maximum size of the shorter URL/code?
        - As Minimum as possible
        - For finding shorter code length, need to check `Back-of-the-envelope` estimation
        - For example, number of requests coming per day and how many years we want service to be running.
        - Let's assume 

            ```
            Number of requests coming per day = 10 million => 10^7
            Number of years = 100

            10 million * 365 days * 100 years = 3650 * 100 Million = 365 Bilion URL

            Let's calculate number of unique short URLs for each length of shorter code:
            number of characters = 62
            If 1 length of character =  _  ==> 62 unique URLs
            If 2 length of character = _ _  ==> 62**2 = 3844 unique URLs
            If 3 length of character = _ _ _  ==> 62**3 = 238328 unique URLs
            ....

            If 6 length of character = _ _ _ _ _ _  ==> 62**6 = 56 Billion unique URLs

            If 7 length of character = _ _ _ _ _ _ _  ==> 62**7 = 3.5 Trillion unique URLs

            So, In our case we need 365 Billion unique URLs, so we can use 7 length of character, as It is generating 3.5 trillion unique URLs
            ```

    - How to generate Hash values?
        - Two ways: 
            - `Using Hash function (MD5 or SHA-256)` 
            - `Using Base62 encoding`

2. *Components:*
    - `Hash Function:`
        - `MD5:` 
            - 128 bit hash value
            - 32 character long hexadecimal string
            - Not reversible
            - Not collision free
        - `SHA-1:`
            - 160 bit hash value
            - 40 character long hexadecimal string
            - Not reversible
            - Not collision free
        - If we take first 7 characters of the has value, chances of `collision` will be very high.
        - So, we can use `Base62 encoding` to generate the shorter URL.
    
    - `Base62 encoding:`
        - As we know, any `Base(10) can be changed to any Base(_)`. Here we need to change Base(10) to Base(62).
        - For example, 1000
            ```
                    62 | 1000     8
                ---------------
                    62 | 16      16
                
                So, 16 8  will be hex, where 16 can be represent as `g` 
                So, 1000 in Base(62) = g8
            ```
        - Here, we can use `Base62 encoding` to generate the shorter URL, but we need to `ID` in advance.
        
    - `ID Generator:`
        - We can use `Auto Increment` ID generator to generate the ID for each URL.

        - `DB with AUTO INCREMENT` column:
            - create seperate DB which keeps auto increment column
            - data generated for couple of days/years are too high, keeping them in single DB can cause following problems:
                - Cost issue to keep IDs in single DB
                - Scalability issues
                - Slowness while fetching the next IDs for each new request
            - So, we can use `Distributed ID generator` to generate the IDs.
            - In `Distributed ID generator`, there is an issue of `Synchronization` can occur.
        
        - So, to solve `synchronization issue` in `Distributed DB`, we can use following methods:
        - 1. `Ticket Service:`
            ```
            App1, App2, App3 -----> Ticket Server ----------> Centralized DB with AUTO
            ```

            - Problem: 
                - Single point of failure
                - Scalability issue
                - Cost issue
        
        - 2. `SnowFlake:`
            - `SnowFlake` is a service which generates unique IDs for each request.
            - It uses `timestamp` and `machine ID` to generate the unique IDs.
            - It is distributed, scalable and cost effective.
            - It is used by Twitter, Uber, etc.
            - It is not reversible.
            - It is not collision free.
        
        - 3. `Zookeeper:`
            - `Zookeeper` is a service which is used to manage distributed systems.
            - It is used to manage the `synchronization` issue in distributed systems.
            - It is used by Apache Kafka, Apache Hadoop, etc.
            - As we know, we have 3.5 trillion unique IDs to generate. In zookeeper, we can create different ranges of IDs for each server.
            - For example, if we have 10 servers, we can create 10 ranges of IDs for each server.
            - Now, each server can generate IDs in its own range. Once the range is exhausted, it can ask for more IDs from zookeeper.
            - This way, we can avoid the `synchronization` issue in distributed systems.

- So, after ID generator, ID is generated, we can use `Base62 encoding` to generate the shorter URL. If number of characters are not enough in Base62 encoding, we can use padding to make it 7 characters long.


### References
1. [Theory](https://youtu.be/C7_--hAhiaM?list=PL6W8uoQQ2c63W58rpNFDwdrBnq5G3EfT7)
2. [API, DB of URL shortening](https://youtu.be/_TsJizByBvE)
            

                
