#!/usr/bin/env python3
"""
ram_cache_estimation_demo.py
---------------------------
Estimate RAM required to cache the last *N* posts for each active user.

Run:
    python ram_cache_estimation_demo.py
"""
from __future__ import annotations

BYTES_IN_GB = 1024 ** 3
CHAR_BYTES = 2


def _prompt_int(prompt: str, default: int) -> int:
    while True:
        raw = input(f"{prompt} [{default}]: ").strip() or str(default)
        try:
            return int(raw.replace("_", ""))
        except ValueError:
            print("❌  Please enter an integer.")


def _fmt_gb(bytes_: float) -> str:
    return f"{bytes_ / BYTES_IN_GB:.2f} GB"


def main() -> None:
    print("\n=== RAM / CACHE ESTIMATOR ===\n")
    dau = _prompt_int("Daily Active Users", 250_000_000)
    posts_cached = _prompt_int("Posts cached per user", 5)
    chars_per_post = _prompt_int("Characters per post", 250)

    bytes_per_post = chars_per_post * CHAR_BYTES
    cache_per_user = bytes_per_post * posts_cached
    total_cache_bytes = cache_per_user * dau

    print("\n--- RESULT ---")
    print(f"Cache per user : {cache_per_user / 1024:.1f} KB")
    print(f"Total cache    : {_fmt_gb(total_cache_bytes)}")

    ram_per_machine_gb = _prompt_int("\nRAM capacity per cache server (GB)", 75)
    machines = total_cache_bytes / (ram_per_machine_gb * BYTES_IN_GB)
    machines = int(machines + 0.999)  # ceiling
    print(f"Cache servers needed: {machines}\n")


if __name__ == "__main__":
    main() 