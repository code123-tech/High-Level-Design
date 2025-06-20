#!/usr/bin/env python3
"""
AP Demo – Availability + Partition-Tolerance (sacrifices Consistency)
--------------------------------------------------------------------
Simulates two replica nodes that continue to accept writes during a
network partition, leading to divergent state. After the partition is
healed we reconcile with a naive 'last write wins' strategy to restore
consistency eventually.
"""

import time
from datetime import datetime

class Node:
    def __init__(self, name):
        self.name = name
        self.data = {"x": 0, "last_ts": 0.0}

    def write(self, key, value):
        ts = time.time()
        self.data[key] = value
        self.data["last_ts"] = ts
        print(f"[{self.name}] ✅  WRITE {key}={value} (ts={ts:.4f})")

    def reconcile(self, other):
        # last write wins
        if other.data["last_ts"] > self.data["last_ts"]:
            self.data = other.data.copy()
            print(f"[{self.name}] 🔄  RECONCILE – adopted other replica state -> {self.data}")
        else:
            print(f"[{self.name}] 🔄  RECONCILE – kept own state -> {self.data}")

    def show_state(self):
        state = {k: v for k, v in self.data.items() if k != "last_ts"}
        print(f"[{self.name}] STATE {state}")


def main():
    print("\n⚖️  AP DEMO – Availability & Partition-Tolerance\n")

    node_a = Node("NodeA")
    node_b = Node("NodeB")

    print("Step 1 – Initial replication (both nodes consistent)")
    node_a.show_state()
    node_b.show_state()

    time.sleep(1)

    print("\nStep 2 – 🔥 Network partition occurs! (Nodes cannot communicate)")

    time.sleep(1)

    print("\nStep 3 – Both sides keep serving writes (stay available)")
    node_a.write("x", 1)
    time.sleep(0.5)
    node_b.write("x", 2)

    time.sleep(1)

    print("\nStep 4 – 🛠️  Partition healed, replicas reconcile (eventual consistency)")
    node_a.reconcile(node_b)
    node_b.reconcile(node_a)

    time.sleep(1)

    print("\n⚠️  Final state – Availability preserved, initial inconsistency resolved via last write wins")
    node_a.show_state()
    node_b.show_state()


if __name__ == "__main__":
    main() 