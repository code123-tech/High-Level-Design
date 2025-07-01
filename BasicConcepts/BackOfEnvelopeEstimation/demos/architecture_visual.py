#!/usr/bin/env python3
"""
architecture_visual.py
----------------------
Tiny helper that prints an ASCII diagram showing how the four BoE calculators
(traffic, storage, RAM, servers) map onto a high-level web-app architecture.

Run:
    python architecture_visual.py
"""

def main() -> None:  # noqa: D401
    diagram = r"""
                +-----------------------------+
                |         Internet            |
                +--------------+--------------+
                               |
                               v
                   +-----------+-----------+
                   |   Load Balancer       |  ← Traffic / QPS calc
                   +-----------+-----------+
                               |
          +--------------------+--------------------+
          |                                         |
          v                                         v
+---------+---------+                     +---------+---------+
|  App Server 1     |      … (N servers)  |  App Server N     |
+---------+---------+                     +---------+---------+
          |                                         |
          +--------------------+--------------------+
                               v
                   +-----------+-----------+
                   |    Cache Layer        |  ← RAM calc
                   +-----------+-----------+
                               |
                               v
                   +-----------+-----------+
                   |  Database / Storage   |  ← Storage calc
                   +-----------------------+

    """
    print(diagram)
    print("Legend:")
    print("  • Traffic / QPS  → estimate peak load hitting LB")
    print("  • RAM            → size in-memory cache for hot data")
    print("  • Storage        → plan DB / object-store capacity")
    print("  • Server count   → number of app servers to meet QPS\n")


if __name__ == "__main__":
    main() 