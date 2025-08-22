# CachingLab — Hands‑on Experiments

Simple, reproducible experiments to learn app‑level caching with Redis and Redis Cluster. For the theory (what, why, pros/cons), read `../../BasicConcepts/Caching/README.md`.

## Menu
- [What you'll do](#-what-youll-do)
- [Prerequisites](#-prerequisites)
- [Single‑node Redis (basic caching)](#1-singlenode-redis-basic-caching)
- [Redis Cluster (consistent hashing)](#2-redis-cluster-consistent-hashing)
- [Tips](#-tips)
- [Cleanup](#-cleanup)

## 📋 What you’ll do
- Run two app instances that share a cache
- Try single Redis (basic caching: miss → hit, cross‑instance sharing)
- Switch to Redis Cluster and verify consistent hashing distribution

## 🧰 Prerequisites
- Docker Desktop running
- PowerShell

Folder: `Projects/CachingLab/`
- `docker-compose.yaml`: Redis (single), Redis Cluster, app1, app2, NGINX LB
- `app.py`: Flask app with Redis client (single or cluster)
- `Dockerfile`, `requirements.txt`
- `configs/lb/nginx.conf`: LB on http://localhost:8080 → app1/app2

---

## 1) Single‑node Redis (basic caching)
By default apps can be set to use the single Redis node.

1) Ensure apps use single Redis
- In `docker-compose.yaml`, under `app1` and `app2`, set:
```
CACHE_BACKEND=single
```

2) Build and start
```powershell
docker compose up -d --build
```
You should see containers: `cache_redis`, `cache_app1` (5000), `cache_app2` (5001), `cache_lb` (8080).

3) Try caching (miss → hit)
```powershell
# Miss then hit (app1)
Measure-Command { curl.exe -s http://localhost:5000/get/foo }  # slower (simulated DB)
Measure-Command { curl.exe -s http://localhost:5000/get/foo }  # fast hit

# Shared cache across instances
curl.exe -s http://localhost:5000/set/bar/999 | Out-Null
curl.exe -s http://localhost:5001/get/bar    # returns 999
```

4) Through LB (round‑robin)
```powershell
1..6 | % { (iwr http://localhost:8080/get/ping -UseBasicParsing).Content }
```

5) Check alternating backends:
```powershell
1..6 | % { curl.exe -sI http://localhost:8080/get/ping | findstr /I X-Upstream }
```

---

## 2) Redis Cluster (consistent hashing)
Switch the apps to use the cluster client and check key distribution across nodes.

1) Point apps to Redis Cluster
- In `docker-compose.yaml`, under `app1` and `app2`, set:
```
CACHE_BACKEND=cluster
```
(Leave the `redis-cluster` service as is.)

2) Recreate (or restart) the stack
```powershell
# From CachingLab folder
docker compose up -d --build
```
You should see `cache_redis_cluster` (ports 7000–7005), `cache_app1`, `cache_app2`, and `cache_lb` up.

3) Insert sample keys via the LB
```powershell
1..20 | % { curl.exe -s "http://localhost:8080/set/k$_/$_" | Out-Null }
Write-Output "Inserted 20 keys via LB"
```

4) Check per‑node key counts (DBSIZE)
```powershell
7000..7005 | % {
  $p=$_;
  $db = docker exec cache_redis_cluster redis-cli -c -p $p dbsize;
  Write-Output "Port $p DBSIZE: $db"
}
```
You should see keys spread across ports 7000–7005 (e.g., 6/5/9/9/6/5).

5) Check hash slots for a few keys
```powershell
$keys = @('k1','k2','k3','foo','bar','baz')
$keys | % {
  $k=$_;
  $slot = docker exec cache_redis_cluster redis-cli -p 7000 CLUSTER KEYSLOT $k;
  Write-Output "Key $k slot $slot"
}
```
Different slots confirm consistent hashing; the client routes each key to the right node.

6) Cross‑instance proof
```powershell
curl.exe -s http://localhost:5000/set/user42/AAA | Out-Null
curl.exe -s http://localhost:5001/get/user42     # returns AAA
```

7) Optional: Hot key simulation and stats
```powershell
1..200 | % { curl.exe -s http://localhost:8080/get/hotkey | Out-Null }
7000..7005 | % {
  $p=$_;
  Write-Output "Port $p"
  docker exec cache_redis_cluster sh -c "redis-cli -p $p INFO stats | grep -E 'keyspace_hits|keyspace_misses' || true"
}
```

---

## Tips
- LB URL: `http://localhost:8080`
- app1: `http://localhost:5000`, app2: `http://localhost:5001`
- If apps fail on first boot (cluster not ready), retry the request; the app lazily initializes with retries.
- To switch modes again, toggle `CACHE_BACKEND` in compose and run:
```powershell
docker compose up -d --build
```

## Cleanup
```powershell
docker compose down -v
```

---

For caching theory (layers, strategies, trade‑offs), see:
- `../../BasicConcepts/Caching/README.md`
