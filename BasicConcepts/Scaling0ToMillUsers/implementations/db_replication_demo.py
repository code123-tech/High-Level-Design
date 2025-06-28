"""
Mini-demo: primary/replica database replication & read-routing
===========================================================
This script simulates the classic production pattern:

    • One *primary* (master) database that accepts **writes**.
    • One or more *replicas* (read-only secondaries) that get changes from the
      primary after a small delay (eventual consistency).
    • An application-side *router* that sends writes to the primary and reads
      to replicas (round-robin in this demo).

Run the file             ::  python db_replication_demo.py
What you'll observe       ::
    1. Write a record to the primary.
    2. Immediate read from a replica is stale (None).
    3. After replication delay the read returns the data.
    4. We add a new replica at runtime; reads are now spread across 3 nodes.

The goal is educational, not performance.  All code is in-memory and single
process so you can step through with a debugger.
"""
from __future__ import annotations

import itertools
import threading
import time
from typing import Dict, List, Sequence


# ---------------------------------------------------------------------------
# Primary / replica implementations
# ---------------------------------------------------------------------------

class PrimaryDB:
    """Primary database that owns the authoritative data & propagates changes."""

    def __init__(self) -> None:
        self._data: Dict[str, str] = {}
        self._replicas: List[ReplicaDB] = []
        self._lock = threading.Lock()

    # -- public API ------------------------------------------------------
    def insert(self, key: str, value: str) -> None:
        with self._lock:
            self._data[key] = value
        self._broadcast("insert", key, value)

    def read(self, key: str) -> str | None:
        return self._data.get(key)

    def attach_replica(self, replica: "ReplicaDB") -> None:
        # 1) send a snapshot so the replica starts consistent
        replica.bulk_load(self._data)
        # 2) add to replication stream for future writes
        self._replicas.append(replica)

    # -- internal helper --------------------------------------------------
    def _broadcast(self, op: str, key: str, value: str | None) -> None:
        for replica in self._replicas:
            replica.enqueue_event(op, key, value)


class ReplicaDB:
    """Read-only replica. Applies events with a fixed network delay."""

    REPLICATION_DELAY_SEC = 0.05  # exaggerate to make staleness visible

    def __init__(self, name: str):
        self.name = name
        self._data: Dict[str, str] = {}
        self._queue: list[tuple[str, str, str | None]] = []
        self._cv = threading.Condition()
        self._thread = threading.Thread(target=self._apply_loop, daemon=True)
        self._thread.start()

    # read-only API ------------------------------------------------------
    def read(self, key: str) -> str | None:
        return self._data.get(key)

    # initial sync ------------------------------------------------------
    def bulk_load(self, snapshot: Dict[str, str]) -> None:
        """Load an initial snapshot before incremental replication begins."""
        self._data.update(snapshot)

    # called by primary ---------------------------------------------------
    def enqueue_event(self, op: str, key: str, value: str | None) -> None:
        with self._cv:
            self._queue.append((op, key, value))
            self._cv.notify()

    # background ---------------------------------------------------------
    def _apply_loop(self) -> None:
        while True:
            with self._cv:
                while not self._queue:
                    self._cv.wait()
                op, key, value = self._queue.pop(0)
            time.sleep(self.REPLICATION_DELAY_SEC)
            if op == "insert":
                self._data[key] = value  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Router – what the application would talk to
# ---------------------------------------------------------------------------

class DatabaseRouter:
    """Routes writes to primary and reads to replicas (round-robin)."""

    def __init__(self, primary: PrimaryDB, replicas: Sequence[ReplicaDB]):
        if not replicas:
            raise ValueError("Need at least one replica for routing demo")
        self._primary = primary
        self._replicas: List[ReplicaDB] = list(replicas)
        self._rr = itertools.cycle(self._replicas)

    # application-facing methods ----------------------------------------
    def write(self, key: str, value: str) -> None:
        print(f"WRITE  → primary    : {key} = {value}")
        self._primary.insert(key, value)

    def read(self, key: str) -> str | None:
        replica = next(self._rr)
        val = replica.read(key)
        print(f"READ   ← {replica.name:<9}: {key} → {val}")
        return val

    # allow scaling reads at runtime ------------------------------------
    def add_replica(self, replica: ReplicaDB) -> None:
        self._primary.attach_replica(replica)
        self._replicas.append(replica)
        self._rr = itertools.cycle(self._replicas)


# ---------------------------------------------------------------------------
# Demo / manual test harness
# ---------------------------------------------------------------------------

def main() -> None:  # noqa: D401 – imperative demo
    primary = PrimaryDB()

    replicas = [ReplicaDB(f"replica-{i}") for i in range(1, 3)]
    for r in replicas:
        primary.attach_replica(r)

    router = DatabaseRouter(primary, replicas)

    # 1) write a record ---------------------------------------------------
    router.write("user:1", "alice")

    # 2) immediate reads are likely stale -------------------------------
    router.read("user:1")
    router.read("user:1")

    # 3) wait for replication lag ---------------------------------------
    print("-- waiting for replication --")
    time.sleep(ReplicaDB.REPLICATION_DELAY_SEC * 2)

    router.read("user:1")
    router.read("user:1")

    # 4) scale reads by adding a new replica ----------------------------
    new_replica = ReplicaDB("replica-3")
    router.add_replica(new_replica)
    time.sleep(ReplicaDB.REPLICATION_DELAY_SEC * 2)

    print("-- after adding replica-3 --")
    router.read("user:1")
    router.read("user:1")
    router.read("user:1")

    router.write("user:2", "bob")

    router.read("user:2")
    router.read("user:2")
    router.read("user:2")
    print("-- waiting for replication --")
    time.sleep(ReplicaDB.REPLICATION_DELAY_SEC * 2)

    router.read("user:2")
    router.read("user:2")
    router.read("user:2")


if __name__ == "__main__":
    main() 