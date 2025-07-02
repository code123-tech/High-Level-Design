#!/usr/bin/env python3
"""load_distribution_demo.py

Simulate how evenly a consistent-hash ring spreads `N` keys over `M` nodes.

You can tweak:
  • number of physical nodes
  • number of virtual nodes per physical node
  • number of keys (requests)

The script prints a text histogram and imbalance percentage.
"""
from __future__ import annotations

import math
import random

from simple_ring import ConsistentHashRing


def _ascii_bar(count: int, max_count: int, width: int = 40) -> str:
    filled = int(count / max_count * width)
    return "█" * filled + "·" * (width - filled)


def main() -> None:
    print("\n🔗  CONSISTENT HASHING – LOAD DISTRIBUTION DEMO\n")
    try:
        nodes = int(input("Number of physical nodes [5]: ") or "5")
        vnodes = int(input("Virtual nodes per physical node [100]: ") or "100")
        requests = int(input("Number of keys/requests to map [100000]: ") or "100000")
    except ValueError:
        print("❌  Invalid integer input. Aborting.")
        return

    ring = ConsistentHashRing(virtual_nodes=vnodes)
    for i in range(1, nodes + 1):
        ring.add_node(f"Node{i}")

    keys = [f"key-{i}-{random.random()}" for i in range(requests)]
    dist = ring.distribution(keys)

    max_count = max(dist.values())
    avg = requests / nodes
    print("\nLoad distribution across nodes:\n")
    for node, cnt in sorted(dist.items()):
        bar = _ascii_bar(cnt, max_count)
        print(f"{node:>6} | {cnt:>8} | {bar}")

    # Standard deviation & imbalance stats
    variance = sum((cnt - avg) ** 2 for cnt in dist.values()) / nodes
    stdev = math.sqrt(variance)
    imbalance_pct = stdev / avg * 100

    print(f"\nMean keys per node   : {avg:.1f}")
    print(f"Standard deviation   : {stdev:.1f}")
    print(f"Imbalance (stdev/avg): {imbalance_pct:.2f} %")
    print("\n✅  Demo complete. Try different parameters to observe the effect of virtual nodes.\n")
    
    print(ring._sorted_keys)


if __name__ == "__main__":
    main() 