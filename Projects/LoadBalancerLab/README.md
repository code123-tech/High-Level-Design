# LoadBalancerLab — Experiments Only

Hands-on lab to explore load-balancing algorithms and behaviors with NGINX and two demo services. For theory, see `../../BasicConcepts/Load_Balancer/README.md`.

## 📋 Menu
- Quick Start (Round Robin)
- Verify Results (PowerShell one-liners)
- Switch Algorithms
  - least_conn
  - ip_hash (sticky)
  - weighted round-robin
- Simulate Failover
- L4 vs L7 Comparison
- Basic Observability
- Cleanup

---

## Quick Start (Round Robin)
Prereqs: Docker Desktop running; PowerShell in this folder (`Projects/LoadBalancerLab`).

Bring up the stack (default mounts `configs/nginx.rr.conf`):
```powershell
docker compose up -d
```

---

## Verify Results (PowerShell one-liners)
Show only the backend server names (L7: port 8080):
```powershell
1..8 | % {
  $h = curl.exe -s http://localhost:8080/
  $m = [regex]::Match($h, 'Server&nbsp;name:</span>\s*<span>([^<]+)</span>', 'IgnoreCase, Singleline')
  if ($m.Success) { $m.Groups[1].Value }
}
```
Count the distribution:
```powershell
(1..40 | % {
  $h = curl.exe -s http://localhost:8080/
  $m = [regex]::Match($h, 'Server&nbsp;name:</span>\s*<span>([^<]+)</span>', 'IgnoreCase, Singleline')
  if ($m.Success) { $m.Groups[1].Value }
}) | Group-Object | Sort-Object Count -Descending
```

L4/TCP passthrough (port 9000):
```powershell
1..8 | % {
  $h = curl.exe -s http://localhost:9000/
  $m = [regex]::Match($h, 'Server&nbsp;name:</span>\s*<span>([^<]+)</span>', 'IgnoreCase, Singleline')
  if ($m.Success) { $m.Groups[1].Value }
}
```
Count on L4:
```powershell
(1..40 | % {
  $h = curl.exe -s http://localhost:9000/
  $m = [regex]::Match($h, 'Server&nbsp;name:</span>\s*<span>([^<]+)</span>', 'IgnoreCase, Singleline')
  if ($m.Success) { $m.Groups[1].Value }
}) | Group-Object | Sort-Object Count -Descending
```

---

## Switch Algorithms
Edit `docker-compose.yaml` to switch the mounted config for the `lb` service (volumes → `nginx.conf`):
- Round Robin: `./configs/nginx.rr.conf`
- Least Connections: `./configs/nginx.least_conn.conf`
- Weighted RR (e.g., 90/10): `./configs/nginx.weighted_rr.conf`
- IP Hash (sticky by client IP): `./configs/nginx.ip_hash.conf`

Apply and reload NGINX:
```powershell
docker compose up -d
docker exec lb_nginx nginx -s reload
```

### least_conn
```powershell
(1..20 | % { $h=curl.exe -s http://localhost:8080/ ; $m=[regex]::Match($h,'Server&nbsp;name:</span>\s*<span>([^<]+)</span>','IgnoreCase,Singleline'); if($m.Success){$m.Groups[1].Value} }) | Group-Object | Sort-Object Count -Descending
```

### ip_hash (sticky)
```powershell
1..8 | % { $h=curl.exe -s http://localhost:8080/ ; $m=[regex]::Match($h,'Server&nbsp;name:</span>\s*<span>([^<]+)</span>','IgnoreCase,Singleline'); if($m.Success){$m.Groups[1].Value} }
```

### weighted round-robin (e.g., 90/10)
```powershell
(1..40 | % { $h=curl.exe -s http://localhost:8080/ ; $m=[regex]::Match($h,'Server&nbsp;name:</span>\s*<span>([^<]+)</span>','IgnoreCase,Singleline'); if($m.Success){$m.Groups[1].Value} }) | Group-Object | Sort-Object Count -Descending
```

---

## Simulate Failover
Enable passive fail behavior in your chosen config by uncommenting:
```
server app1:80 max_fails=2 fail_timeout=5s;
server app2:80 max_fails=2 fail_timeout=5s;
```
Reload NGINX, then stop a backend:
```powershell
docker exec lb_nginx nginx -s reload
docker stop lb_app1
1..10 | % { $h=curl.exe -s http://localhost:8080/ ; $m=[regex]::Match($h,'Server&nbsp;name:</span>\s*<span>([^<]+)</span>','IgnoreCase,Singleline'); if($m.Success){$m.Groups[1].Value} }
```

---

## L4 vs L7 Comparison
- L7 (HTTP-aware): http://localhost:8080
- L4 (TCP passthrough): http://localhost:9000 (configured in the `stream {}` block)

L4 test:
```powershell
1..8 | % { $h=curl.exe -s http://localhost:9000/ ; $m=[regex]::Match($h,'Server&nbsp;name:</span>\s*<span>([^<]+)</span>','IgnoreCase,Singleline'); if($m.Success){$m.Groups[1].Value} }
```

---

## Basic Observability
- NGINX stub status:
```powershell
curl http://localhost:8080/nginx_status
```
- Tail LB access logs:
```powershell
docker exec -it lb_nginx sh -c "tail -n 50 /var/log/nginx/access.log"
```

---

## Cleanup
```powershell
docker compose down -v
```

---

Notes
- Backends are named `app1` and `app2`, so the demo page prints `Server name: app1/app2` for easy identification.
- If you add more backends/configs, reuse the verification snippets above.

