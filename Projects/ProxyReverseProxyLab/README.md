# ProxyReverseProxyLab

Build, run, and play with a reverse proxy (NGINX) in front of two tiny apps. Learn canary (90/10), caching, and rate limiting—step by step.

---

## Menu

- [1) What are we building?](#1-what-are-we-building)
- [2) One-time setup](#2-one-time-setup)
- [3) Start the lab](#3-start-the-lab)
- [4) Try it out (copy/paste tests)](#4-try-it-out-copypaste-tests)
- [5) How it works (simple words)](#5-how-it-works-simple-words)
- [6) Files you can read](#6-files-you-can-read)
- [7) Stop the lab](#7-stop-the-lab)
- [8) Future scope](#8-future-scope)

## 1) What are we building?

- A friendly traffic cop called a "reverse proxy" (NGINX)
- Two small app workers: `app-v1` and `app-v2`
- NGINX sends most cars (requests) to `v1` and a few to `v2` (canary)
- NGINX can remember answers for a short time (cache)
- NGINX can slow down pushy visitors (rate limit)

Picture:

```
You --> NGINX (port 8080) --> [ app-v1 (90%) | app-v2 (10%) ]
```

---

## 2) One-time setup

You need Docker and Docker Compose. On Windows, install Docker Desktop.

---

## 3) Start the lab

Open a terminal in this folder and run:

```powershell
docker compose up --build
```

When it finishes, open this in your browser:

- `http://localhost:8080/` → hello message
- `http://localhost:8080/api/items` → the app data
- `http://localhost:8080/nginx_status` → NGINX stats

Tip for Windows: Use `curl.exe` (not PowerShell's alias) if you copy the commands below.

---

## 4) Try it out (copy/paste tests)

### A) Canary rollout (most to v1, a few to v2)

Use PowerShell-safe commands. We also add a random `?t=` to skip the cache so you can see the split clearly.

- Easiest (parses JSON directly):
```powershell
1..30 | ForEach-Object { (Invoke-RestMethod -Uri "http://localhost:8080/api/items?t=$([guid]::NewGuid())" -TimeoutSec 10).version }
```

- If you prefer curl output and searching text:
```powershell
1..30 | ForEach-Object { curl.exe -s "http://localhost:8080/api/items?t=$([guid]::NewGuid())" | Select-String -Pattern '"version"' }
```

- If you want to use findstr specifically (quote safely in PowerShell):
```powershell
1..30 | ForEach-Object { curl.exe -s "http://localhost:8080/api/items?t=$([guid]::NewGuid())" | findstr /C:'"version"' }
```

You should see mostly `"v1"` and sometimes `"v2"` (about 90/10).

### B) Caching (second call is faster)

```powershell
Measure-Command { curl.exe -s http://localhost:8080/api/items | Out-Null }
Measure-Command { curl.exe -s http://localhost:8080/api/items | Out-Null }
```

The second command should be faster. You can also check the cache header:

```powershell
curl.exe -s -D - http://localhost:8080/api/items -o NUL | findstr X-Cache-Status
# or
curl.exe -s -D - http://localhost:8080/api/items -o NUL | Select-String -Pattern "X-Cache-Status"
```

You should see `X-Cache-Status: HIT` after the first fetch.

### C) Rate limiting (too many requests get 429)

```powershell
1..40 | ForEach-Object { curl.exe -s -o NUL -w "%{http_code}`n" http://localhost:8080/api/items }
```

Some responses will show `429` (Too Many Requests).

Parallel test (more visible throttling):

- PowerShell 7+
```powershell
1..40 | ForEach-Object -Parallel { curl.exe -s -o NUL -w "%{http_code}`n" "http://localhost:8080/api/items?t=$([guid]::NewGuid())" } -ThrottleLimit 40
```

- Windows PowerShell 5.x
```powershell
$jobs = 1..40 | ForEach-Object { Start-Job { param($u) curl.exe -s -o NUL -w "%{http_code}`n" $u } -ArgumentList "http://localhost:8080/api/items?t=$([guid]::NewGuid())" }
$jobs | Receive-Job -Wait -AutoRemoveJob
```

Tip: The random `?t=` parameter bypasses NGINX cache so you see true rate limiting.

---

## 5) How it works (simple words)

- **Reverse proxy (NGINX)**: A smart gateway that receives your request and decides where to send it.
- **Canary**: Send 90% to `v1` and 10% to `v2` using weights. That lets you test a new version safely.
- **Cache**: Keep answers for a short time (60 seconds) so repeated questions are served instantly.
- **Rate limit**: If someone asks too fast, slow them down or say "429: too many requests".
- **Forwarded headers**: NGINX adds `X-Forwarded-For` and friends so the app knows the real client.

---

## 6) Files you can read

- `docker-compose.yml`: Starts NGINX and two app containers.
- `reverse-proxy/nginx.conf`: The NGINX brain (canary, caching, rate limit, status page).
- `app/main.py`: The tiny FastAPI app that returns items and shows its version.

---

## 7) Stop the lab

```powershell
docker compose down
```

To also clear the NGINX cache volume:

```powershell
docker compose down -v
```

---

## 8) Future scope

- TLS + HTTP/2 at the edge
  - What: Serve HTTPS on a new port (e.g., 8443) using self‑signed certs; enable HTTP/2
  - Why: Realistic edge termination and H2 multiplexing

- Prometheus metrics for NGINX
  - What: Add `nginx-prometheus-exporter` and scrape `stub_status`; create Grafana panels
  - Why: Observe edge latency, cache hit ratio, and 429 rates over time

- Sticky/header-based canary
  - What: Route to v2 when header `X-Canary: true` (or a cookie) while keeping 90/10 default
  - Why: Targeted rollouts and simple session stickiness

- WebSocket pass-through
  - What: Add a FastAPI `ws://` endpoint and configure `Upgrade`/`Connection` headers in NGINX
  - Why: Demonstrate realtime proxying

- Smarter caching with ETag + revalidation
  - What: App emits `ETag`; NGINX uses `proxy_cache_revalidate`; optional cache purge endpoint
  - Why: Correct freshness with minimal bandwidth (304 responses)

- Friendly error pages and JSON 429 body
  - What: Custom `error_page` for 429/5xx with small JSON bodies
  - Why: Better developer experience and observability


