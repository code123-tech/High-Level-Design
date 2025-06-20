#!/usr/bin/env python3
"""
practical_examples.py
=====================
Mini showcase mapping real-world databases / services to CP or AP side of
CAP.  This is not meant to be a faithful implementation—just an
illustrative, runnable script that prints behavior patterns.

Run directly or via README guidance.
"""

import time
from random import choice, random

class HBaseLikeCP:
    """Simulate CP-oriented store: strong consistency, may reject writes."""
    def __init__(self):
        self.data = {}
        self.primary_up = True

    def write(self, key, value):
        if not self.primary_up:
            print("[HBase-CP] ❌  PRIMARY DOWN – write rejected to maintain consistency")
            return False
        self.data[key] = value
        print(f"[HBase-CP] ✅  write {key}={value}")
        return True

    def read(self, key):
        print(f"[HBase-CP] 📖 read {key} -> {self.data.get(key)}")

class CassandraLikeAP:
    """Simulate AP-oriented store: always accepts writes, eventual consistency."""
    def __init__(self):
        self.replicas = [{}, {}]  # two replicas diverge

    def write(self, key, value):
        target = choice(self.replicas)  # whichever replica client hits
        target[key] = value
        print(f"[Cassandra-AP] ✅ write {key}={value} on replica id={id(target)%1000}")

    def read(self, key):
        # read from random replica (may be stale)
        src = choice(self.replicas)
        print(f"[Cassandra-AP] 📖 read {key}={src.get(key)} from replica id={id(src)%1000}")

    def anti_entropy(self):
        """Periodic background sync (simplified)"""
        consolidated = {}
        for r in self.replicas:
            consolidated.update(r)
        for r in self.replicas:
            r.update(consolidated)
        print("[Cassandra-AP] 🔄 anti-entropy pass complete – replicas converged")


def demo_hbase_vs_cassandra():
    print("\n🏛️  PRACTICAL EXAMPLE – HBase (CP) vs Cassandra (AP)\n")

    cp_store = HBaseLikeCP()
    ap_store = CassandraLikeAP()

    cp_store.write("order123", "PENDING")
    ap_store.write("order123", "PENDING")

    # Simulate failure of CP primary
    cp_store.primary_up = False
    print("\n⚡ Network partition / primary failure…")
    cp_store.write("order123", "CONFIRMED")  # gets rejected
    ap_store.write("order123", "CONFIRMED")   # accepted on one replica

    # Reads show difference
    cp_store.read("order123")
    ap_store.read("order123")

    print("\n🛠️  Repair / anti-entropy phase…")
    ap_store.anti_entropy()
    cp_store.primary_up = True
    cp_store.write("order123", "CONFIRMED")   # now succeeds after recovery

    # Final reads
    cp_store.read("order123")
    ap_store.read("order123")


def main():
    demo_hbase_vs_cassandra()

if __name__ == "__main__":
    main() 