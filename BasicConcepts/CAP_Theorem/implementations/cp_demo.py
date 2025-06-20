#!/usr/bin/env python3
"""
CP Demo – Consistency + Partition-Tolerance (sacrifices Availability)
--------------------------------------------------------------------
A minimal, self-contained simulation that illustrates why a CP system
will refuse writes on the minority side of a partition to preserve
strong consistency.

Run this file directly or via the CAP_Theorem/quick_start.py menu.
"""

import time
from datetime import datetime

class Node:
    def __init__(self, name):
        self.name = name
        self.data = {"x": 0}
        self.available_for_writes = True  # will become False on partition

    def write(self, key, value):
        if not self.available_for_writes:
            print(f"[{self.name}] ❌  WRITE REJECTED (node unavailable for writes)")
            return
        self.data[key] = value
        print(f"[{self.name}] ✅  WRITE {key}={value}")

    def sync_from(self, other):
        self.data.update(other.data)
        print(f"[{self.name}] 🔄  SYNC completed -> {self.data}")

    def show_state(self):
        print(f"[{self.name}] STATE {self.data}")


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def main():
    print("\n⚖️  CP DEMO – Consistency & Partition-Tolerance\n")

    node_a = Node("NodeA")
    node_b = Node("NodeB")

    print("Step 1 – Initial replication (both nodes consistent)")
    node_a.show_state()
    node_b.sync_from(node_a)
    node_b.show_state()

    time.sleep(1)

    print("\nStep 2 – 🔥 Network partition occurs! (Nodes cannot communicate)")
    node_b.available_for_writes = False  # simulate minority side made read-only

    time.sleep(1)

    print("\nStep 3 – Client writes to NodeA → allowed (majority)")
    node_a.write("x", 1)

    time.sleep(1)

    print("\nStep 4 – Client tries to write to NodeB → rejected (unavailable)")
    node_b.write("x", 2)

    time.sleep(1)

    print("\nStep 5 – 🛠️  Partition healed, replicas resynchronise")
    node_b.available_for_writes = True
    node_b.sync_from(node_a)

    time.sleep(1)

    print("\n✅ Final state – Consistency preserved, NodeB experienced downtime")
    node_a.show_state()
    node_b.show_state()


if __name__ == "__main__":
    main() 