from flask import Flask
import os, time, random

CACHE_BACKEND = os.getenv('CACHE_BACKEND', 'single')

app = Flask(__name__)

_cache_client = None

def _init_cache_with_retry():
    global _cache_client
    if _cache_client is not None:
        return _cache_client

    attempts = 0
    last_err = None
    while attempts < 30:  # ~30 seconds max with 1s sleep
        try:
            if CACHE_BACKEND == 'cluster':
                # Redis 5 client provides RedisCluster
                from redis.cluster import RedisCluster
                client = RedisCluster(
                    host='redis-cluster',
                    port=7000,
                    decode_responses=True,
                    socket_timeout=2,
                    skip_full_coverage_check=True,
                )
            else:
                from redis import Redis
                client = Redis(host='redis', port=6379, db=0, decode_responses=True, socket_timeout=2)
            # simple ping to verify connectivity
            client.ping()
            _cache_client = client
            return _cache_client
        except Exception as e:
            last_err = e
            attempts += 1
            time.sleep(1)
    # If we exit the loop, raise the last error
    raise RuntimeError(f"Failed to connect to cache after {attempts} attempts: {last_err}")

DB_SIM_DELAY = 0.5

@app.route('/get/<key>')
def get_value(key: str):
    cache = _init_cache_with_retry()
    val = cache.get(key)
    if val is None:
        time.sleep(DB_SIM_DELAY)
        val = str(random.randint(1, 1000))
        cache.set(key, val, ex=30)
    return val

@app.route('/set/<key>/<val>')
def set_value(key: str, val: str):
    cache = _init_cache_with_retry()
    cache.set(key, val, ex=30)
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)