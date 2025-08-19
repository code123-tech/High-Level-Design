# High Level Design 🏗️
Basic concepts, learning materials, and practical implementations for High Level Design

## 📋 Table of Contents

### 🚀 Quick Navigation
- [🎯 Quick Start Guide](#-quick-start-guide)
- [📚 Learning Structure](#-learning-structure)
- [🎯 Practice Questions](#-practice-questions)
- [📖 References & Resources](#-references--resources)
- [🎯 Learning Path Recommendation](#-learning-path-recommendation)

### 📚 Basic Concepts
- [🏛️ Client-Server vs P2P - Complete Architecture Hub](#️-client-server-vs-peer-to-peer---complete-architecture-hub)
- [⚖️ CAP Theorem - Complete Learning Hub](#-cap-theorem---complete-learning-hub)
- [🏗️ Microservices Design Patterns - Complete Learning Hub](#-microservices-design-patterns---complete-learning-hub)
- [🌐 Network Protocols - Complete Learning Hub](#-network-protocols---complete-learning-hub)
- [🚦 Load Balancers - Complete Learning Hub](#-load-balancers---complete-learning-hub)
- [📈 Scalling 0 to million users Guide](#-scaling-0-to-million-users-guide)
- [🧮 Back of the Envelop Estimation](#-back-of-the-envelop-estimation)
- [🛢️ SQL v/s NoSQL - When to use which](#-sql-vs-nosql---when-to-use-which)
- [🧭 Architecture Guide](#-architecture-guide)
- [📨 Distributed Message Queue, Kafka](#-distributed-message-queue-kafka)
- [🔀 Proxy_Reverse Proxy](#-proxy_reverse-proxy)
- [🔧 Additional HLD Components](#-additional-hld-components-coming-soon)
- [🗃️ Database Concepts](#️-database-concepts-coming-soon)

### 🎯 Practice Questions by Difficulty
- [Easy Questions](#easy-questions)
- [Medium Questions](#medium-questions)
- [Hard Questions](#hard-questions)

### 🛠️ Practical Commands
- [Network Protocols Commands](#for-network-protocols-learning)
- [Architecture Patterns Commands](#for-architecture-patterns-learning)
- [CAP Theorem Commands](#for-cap-theorem-learning)
- [System Design Practice](#for-system-design-practice)

---

### [Basic Concepts](./BasicConcepts/)

#### 🏛️ [Client-Server vs Peer-to-Peer - Complete Architecture Hub](./BasicConcepts/ClientServer_P2P/)
**Comprehensive practical learning for fundamental network architectures**

📁 **Organized Structure:**
- 🛠️ **Implementations**: Working Client-Server and P2P demos
- 🎮 **Demos**: Interactive architecture comparison tools
- 🚀 **Examples**: Real-world systems (Banking, Web, BitTorrent, Blockchain)
- ⚡ **Quick Start**: Interactive architecture learning guide

**🚀 Get Started:**
```bash
cd BasicConcepts/ClientServer_P2P
python quick_start.py
```

#### ⚖️ [CAP Theorem - Complete Learning Hub](./BasicConcepts/CAP_Theorem/)
**Hands-on simulations demonstrating CP vs AP trade-offs**

📁 **Organized Structure:**
- 🛠️ **Implementations**: `cp_demo.py`, `ap_demo.py` (and optional `ca_demo.py`)
- 📊 **Comparison Tool**: Side-by-side output viewer
- 🚀 **Examples**: Real-world CP vs AP showcase
- ⚡ **Quick Start**: Interactive learning guide

**🚀 Get Started:**
```bash
cd BasicConcepts/CAP_Theorem
python quick_start.py
```

#### 🏗️ [Microservices Design Patterns - Complete Learning Hub](./BasicConcepts/Microservices_DesignPatterns/)
**Interactive demos for Strangler, SAGA, CQRS and other key patterns**

📁 **Organized Structure:**
- 🛠️ **Implementations**: `strangler_demo.py`, `saga_demo.py`, `cqrs_demo.py`
- 🎮 **Demos**: Pattern comparison tool (placeholder)
- 🚀 **Examples**: Real-world snippets (TBD)
- ⚡ **Quick Start**: Interactive learning guide

**🚀 Get Started:**
```bash
cd BasicConcepts/Microservices_DesignPatterns
python quick_start.py
```

#### 🌐 [Network Protocols - Complete Learning Hub](./BasicConcepts/NetworkProtocols/)
**Comprehensive practical learning for TCP, UDP, HTTP, and WebSockets**

📁 **Organized Structure:**
- 🛠️ **Implementations**: Individual protocol examples (TCP, UDP, HTTP)
- 🎮 **Demos**: Protocol comparison tools
- 🚀 **Examples**: Real-world projects (Chat app, Game server, Web API)
- ⚡ **Quick Start**: Interactive learning guide

**🚀 Get Started:**
```bash
cd BasicConcepts/NetworkProtocols
python3 quick_start.py
```

#### 🚦 [Load Balancers - Complete Learning Hub](./BasicConcepts/Load_Balancer/)
**End-to-end guide to L4/L7 load balancing, algorithms, health checks, TLS, and HA deployments**

📁 **Organized Structure:**
- 📖 **Guide**: Concepts with diagrams (this README)
- 🧪 **Experiments**: (TBD) NGINX/HAProxy/Envoy snippets

**🚀 Get Started:**
```bash
cd BasicConcepts/Load_Balancer
# Read the guide
code README.md
```

#### 📈 [Scaling 0 to million users Guide](./BasicConcepts/Scaling0ToMillUsers/)
**Comprehensive practical learning for Load balancers, DB replication etc.

📁 **Organized Structure:**
- 🛠️ **Implementations**: Individual step demo can be used to handle million users
- 🎮 **Demos**: Protocol comparison tools
- ⚡ **Quick Start**: Interactive learning guide

**🚀 Get Started:**
```bash
cd BasicConcepts/Scaling0ToMillUsers
python3 quick_start.py
```

- [Guide for scaling concepts](./BasicConcepts/Scaling0ToMillUsers.md)
- [Consistent Hashing](./BasicConcepts/Consistent_Hashing.md)
- [Back of the envelope estimation](./BasicConcepts/Back_Of_The_Envelop_Esitmation.md)


#### 🧮 [Back of the Envelop Estimation](./BasicConcepts/BackOfEnvelopeEstimation/)
**Back-of-the-envelope (BoE) maths is about turning coarse assumptions into
order-of-magnitude numbers *fast* (≈10 min).

📁 **Organized Structure:**
- 🛠️ **Implementations**: Individual step demo can be used to handle million users
- 🎮 **Demos**: Architectural visual tools
- ⚡ **Quick Start**: Interactive learning guide

**🚀 Get Started:**
```bash
cd BasicConcepts/BackOfEnvelopeEstimation
python3 quick_start.py
```

#### 🛢️ [SQL v/s NoSQL - When to use which](./BasicConcepts/SQL_VS_NOSQL/)
This is a detailed guide on when to use SQL and when to use NoSQL with some demos.

📁 **Organized Structure:**
- 🛠️ **Implementations**: Various demos showing the difference between SQL and NoSQL
- ⚡ **Quick Start**: Interactive learning guide

**🚀 Get Started:**
```bash
cd BasicConcepts/SQL_VS_NOSQL
python3 quick_start.py
```

#### 🧭 [Architecture Guide](./BasicConcepts/Architecture_Guide/)
This is a detailed guide on how to design an architecture for a given problem.

📁 **Organized Structure:**
- 🛠️ **Implementations**: Various demos showing the difference between SQL and NoSQL

**🚀 Get Started with theory:**
```bash
cd BasicConcepts/ArchitectureGuide
```

**🚀 Get Started with practical:**
```bash
cd Projects/ArchitecturePatterns
docker-compose -f docker/single-node/docker-compose.yml up -d
```

#### 📨 [Distributed Message Queue, Kafka](./BasicConcepts/Distributed_Messaging_Queue/)
This is a detailed guide on how to design a distributed message queue using Kafka.  

**🚀 Get Started with theory:**
```bash
cd BasicConcepts/Distributed_Messaging_Queue
```

**🚀 Get Started with practical:**

1. Basic Point to Point Messaging with RabbitMQ
```bash
cd Projects/MessageQueueExperiments/basic_point_to_point
python3 producer.py
python3 consumer.py
```

#### 🔀 [Proxy_Reverse Proxy](./BasicConcepts/Proxy_ReverseProxy/)
This is a detailed guide on how to design a proxy and reverse proxy.  

**🚀 Get Started with theory:**
```bash
cd BasicConcepts/Proxy_ReverseProxy
```

**🚀 Get Started with practical:**

1. Build, run, and play with a reverse proxy (NGINX) in front of two tiny apps. Learn canary (90/10), caching, and rate limiting—step by step.

Project: [ProxyReverseProxyLab](./Projects/ProxyReverseProxyLab/)
```bash
cd Projects/ProxyReverseProxyLab
docker-compose up -d

# Test it
curl http://localhost:8080/
curl http://localhost:8080/api/v1/hello

# Stop it
docker-compose down
```

#### 🔧 Additional HLD Components (Coming Soon)
- Storage types: (Block, File, Object storage, RAID)
- File System (Google file system, HDFS)
- Bloom Filter
- Merkle Tree, Gossiping Protocol
- Caching (Cache invalidation, cache eviction)

#### 🗃️ Database Concepts (Coming Soon)
- Sharding
- Partitioning
- Replication, Mirroring
- Leader Election
- Indexing

## 🎯 [Practice Questions](./Questions/)

### Easy Questions
| Question | Status |
| --- | --- |
| [Design URL Shortening](./Questions/URL_Shortening/) | :white_check_mark: |
| Design Pastebin | &#9744; |

### Medium Questions
| Question | Status |
| --- | --- |
| [Design Consistent Hashing](./Questions/Consistent%20Hashing%20Implementation/) | :white_check_mark: |
| [Design Key-Value Store](./Questions/Key-Value_Store/) | :construction: |
| [Design Rate Limiter](./Questions/DesignRateLimiter/) | :construction: |
| Design Search Autocomplete/TypeAhead System | &#9744; |
| Design Notification System | &#9744; |
| Design Web Crawler | &#9744; |
| Design Nearby Friends/Yelp | &#9744; |

### Hard Questions
| Question | Status |
| --- | --- |
| [Design Chat System (WhatsApp)](./Questions/DesignChatSystem(WhatsApp)/) | :white_check_mark: |
| Design Twitter | &#9744; |
| Design Dropbox | &#9744; |
| Design Instagram | &#9744; |
| Design Youtube | &#9744; |
| Design Google Drive | &#9744; |
| Design Facebook News Feed | &#9744; |
| Design Ticket Master | &#9744; |

## 🚀 Quick Start Guide

### For Network Protocols Learning:
```bash
# Interactive learning experience
cd BasicConcepts/NetworkProtocols
python3 quick_start.py

# Try individual protocols
python3 implementations/tcp_implementation.py
python3 implementations/udp_implementation.py
python3 implementations/http_implementation.py

# Real-world projects
python3 examples/practical_projects.py
```

### For Architecture Patterns Learning:
```bash
# Interactive architecture comparison
cd BasicConcepts/ClientServer_P2P
python quick_start.py

# Try individual architectures
python implementations/client_server_demo.py
python implementations/peer_to_peer_demo.py

# Real-world examples
python examples/practical_examples.py
```

### For System Design Practice:
1. Start with **Basic Concepts** to build foundation
2. Practice with **Network Protocols** implementations
3. Solve **Questions** to test understanding

### For CAP Theorem Learning:
```bash
# Interactive CAP experience
cd BasicConcepts/CAP_Theorem
python quick_start.py

# Compare CP vs AP side-by-side
python demos/cap_comparison.py

# Run demos individually
python implementations/cp_demo.py
python implementations/ap_demo.py
```

### For Microservices Design Patterns Learning:
```bash
cd BasicConcepts/Microservices_DesignPatterns
python quick_start.py
```

### For Back of Envelope Estimation Learning:
```bash
cd BasicConcepts/BackOfEnvelopeEstimation
python quick_start.py
```

## 📖 References & Resources

- [System Design Interview YouTube Playlist](https://www.youtube.com/watch?v=rliSgjoOFTs&list=PL6W8uoQQ2c63W58rpNFDwdrBnq5G3EfT7)
- [System Design Primer](http://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)

## 🎯 Learning Path Recommendation

1. **Foundation** (Week 1-2)
   - Network Protocols (with hands-on coding)
   - Client-Server vs P2P Architecture (with practical examples)
   - CAP Theorem

2. **Scaling & Performance** (Week 3-4)
   - Scaling strategies
   - Consistent Hashing
   - Back-of-envelope estimation

3. **Design Patterns** (Week 5-6)
   - Microservices patterns
   - Database concepts

4. **Practice** (Week 7+)
   - Solve system design questions
   - Build real projects

---

**Happy Learning! 🎉** Start with the Network Protocols section for hands-on experience!

