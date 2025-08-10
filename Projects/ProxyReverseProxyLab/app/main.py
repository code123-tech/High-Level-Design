import os
import socket
import time
from typing import List

from fastapi import FastAPI

app = FastAPI(title="Proxy/Reverse Proxy Demo App")


def get_version() -> str:
    return os.getenv("APP_VERSION", "v1")


@app.get("/")
def root():
    return {
        "message": "Hello from the demo app",
        "version": get_version(),
        "hostname": socket.gethostname(),
        "hint": "Use /api/items to see canary and caching via the reverse proxy"
    }


@app.get("/health")
def health():
    return {"status": "healthy", "version": get_version()}


@app.get("/api/items")
def get_items(count: int = 5):
    # Simulate work to make cache benefits visible
    time.sleep(0.3)
    count = max(1, min(count, 50))
    items = [
        {"id": i, "name": f"item-{i}", "version": get_version()}
        for i in range(1, count + 1)
    ]
    return {"items": items, "version": get_version()}


