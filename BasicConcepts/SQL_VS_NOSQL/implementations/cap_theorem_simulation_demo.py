#!/usr/bin/env python3
"""
cap_theorem_simulation_demo.py

Demo: Simulate the CAP theorem in a distributed system.

- Simulates two nodes and a network partition.
- Shows how SQL (CA) and NoSQL (AP/CP) systems might behave during a partition.

This script is for learning purposes and does not require any external database.
"""
import time

# Simulate two nodes with a partition flag
def simulate_cap_theorem():
    print("\n--- CAP Theorem Simulation Demo ---")
    # Initial state: both nodes in sync
    node1 = {"value": 100}
    node2 = {"value": 100}
    print(f"Initial state: node1={node1}, node2={node2}")

    # Simulate network partition
    partitioned = True
    print("\n[Network partition occurs! Nodes cannot communicate.]")

    # SQL-like system: blocks writes to maintain consistency
    print("\nSQL-like system (CA): Blocks writes during partition to maintain consistency.")
    try:
        if partitioned:
            raise Exception("Network partition: Cannot guarantee consistency. Blocking writes.")
    except Exception as e:
        print(f"Write attempt blocked: {e}")
    print(f"State after blocked write: node1={node1}, node2={node2}")

    # NoSQL-like system: allows writes, risking inconsistency
    print("\nNoSQL-like system (AP): Allows writes during partition (eventual consistency).")
    print("Writing 120 to node1 and 80 to node2 (conflicting updates)...")
    if partitioned:
        node1["value"] = 120
        node2["value"] = 80
    print(f"State during partition: node1={node1}, node2={node2}")

    # Partition heals, nodes sync (eventual consistency)
    print("\n[Partition heals. Nodes synchronize (eventual consistency)...]")
    time.sleep(1)
    # Resolve conflict (choose max value for demo)
    resolved_value = max(node1["value"], node2["value"])
    node1["value"] = node2["value"] = resolved_value
    print(f"State after sync: node1={node1}, node2={node2}")
    print("\n✅  Demo complete. Notice the trade-offs: SQL blocks to preserve consistency, NoSQL allows availability but risks temporary inconsistency.")

if __name__ == "__main__":
    simulate_cap_theorem() 