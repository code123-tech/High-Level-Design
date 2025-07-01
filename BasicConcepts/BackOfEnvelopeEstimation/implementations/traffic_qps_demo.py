#!/usr/bin/env python3
"""
traffic_qps_demo.py
-------------------
Interactive calculator that estimates queries per second (QPS) from basic
usage assumptions.  You provide:
  • Daily Active Users (DAU)
  • Average READ ops per user per day
  • Average WRITE ops per user per day

Run:
    python traffic_qps_demo.py
Press CTRL-C to quit at any time.
"""
from __future__ import annotations

SECONDS_IN_DAY_SIMPLIFIED = 100_000  # BoE-friendly round number


def _prompt_int(prompt: str, default: int) -> int:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or str(default)
        try:
            return int(raw.replace("_", ""))
        except ValueError:
            print("❌  Please enter a valid integer.")


def main() -> None:  # noqa: D401 – imperative CLI
    print("\n=== TRAFFIC / QPS ESTIMATOR ===\n")
    dau = _prompt_int("Daily Active Users", 250_000_000)
    reads_per_user = _prompt_int("Avg READ queries per user per day", 5)
    writes_per_user = _prompt_int("Avg WRITE queries per user per day", 2)

    total_queries_day = dau * (reads_per_user + writes_per_user)
    qps = total_queries_day / SECONDS_IN_DAY_SIMPLIFIED

    print("\n--- RESULT ---")
    print(f"Total queries per day : {total_queries_day:,.0f}")
    print(
        f"QPS (approx)          : {qps:,.0f} req/s  "
        f"(assuming {SECONDS_IN_DAY_SIMPLIFIED:,} s/day)"
    )
    print("-----------------------\n")


if __name__ == "__main__":
    main() 