#!/usr/bin/env python3
"""
server_estimation_demo.py
-------------------------
Mini-calculator that determines how many application servers you need to
satisfy a target QPS given latency and threads per server.

Run:
    python server_estimation_demo.py
"""
from __future__ import annotations


def _prompt_float(prompt: str, default: float) -> float:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or str(default)
        try:
            return float(raw)
        except ValueError:
            print("❌  Please enter a number.")


def _prompt_int(prompt: str, default: int) -> int:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or str(default)
        try:
            return int(raw.replace("_", ""))
        except ValueError:
            print("❌  Please enter an integer.")


def main() -> None:  # noqa: D401
    print("\n=== SERVER COUNT ESTIMATOR ===\n")
    qps = _prompt_float("Target QPS", 18_000)
    latency_ms = _prompt_float("Latency per request (ms)", 500.0)
    threads = _prompt_int("Threads per server", 50)

    req_per_thread = 1000 / latency_ms  # 500ms → 2 req/s
    req_per_server = req_per_thread * threads
    servers = int((qps / req_per_server) + 0.999)  # ceiling

    print("\n--- RESULT ---")
    print(f"Each server handles ≈ {req_per_server:.1f} req/s")
    print(f"Servers needed  : {servers}")
    print("(Add redundancy and headroom for real deployments.)\n")


if __name__ == "__main__":
    main() 