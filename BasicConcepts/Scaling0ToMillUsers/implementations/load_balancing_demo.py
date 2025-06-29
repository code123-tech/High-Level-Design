"""
load_balancing_demo.py
----------------------
Mini-simulation of a round-robin load balancer distributing requests across a
pool of backend servers. Run:
    python load_balancing_demo.py

Sample output (abbreviated):
    Processing req  1 → backend-1
    Processing req  2 → backend-2
    Processing req  3 → backend-3
    Processing req  4 → backend-1
    ...

The demo then adds a new server and removes one to show dynamic scaling.
"""
from __future__ import annotations

import itertools
import random
import time
from typing import Iterable, List


class BackendServer:
    """Toy backend – sleeps a bit to mimic work and prints its name."""

    def __init__(self, name: str) -> None:
        self.name = name

    def handle(self, request_id: int) -> None:
        work_ms = random.uniform(10, 50)  # 10-50 ms
        time.sleep(work_ms / 1000)
        print(f"Processing req {request_id:2} → {self.name}")


class RoundRobinLoadBalancer:
    """Very small round-robin scheduler."""

    def __init__(self, backends: Iterable[BackendServer]):
        self._backends: List[BackendServer] = list(backends)
        if not self._backends:
            raise ValueError("Must provide at least one backend")
        self._iterator = itertools.cycle(self._backends)

    # Public API ----------------------------------------------------------
    def route(self, request_id: int) -> None:
        backend = next(self._iterator)
        backend.handle(request_id)

    def add_backend(self, backend: BackendServer) -> None:
        self._backends.append(backend)
        self._iterator = itertools.cycle(self._backends)

    def remove_backend(self, name: str) -> None:
        self._backends = [b for b in self._backends if b.name != name]
        if not self._backends:
            raise RuntimeError("No backends left!")
        self._iterator = itertools.cycle(self._backends)


# ----------------------------------------------------------------------
# Alternative algorithm: least-connections (tracks in-flight requests)
# ----------------------------------------------------------------------


class LeastConnectionsLoadBalancer:
    """Picks the backend with the fewest *currently in-flight* requests."""

    def __init__(self, backends: Iterable[BackendServer]):
        self._backends: List[BackendServer] = list(backends)
        if not self._backends:
            raise ValueError("Must provide at least one backend")
        # Map backend-name → current in-flight count
        self._inflight: dict[str, int] = {b.name: 0 for b in self._backends}

    # Public API ------------------------------------------------------
    def route(self, request_id: int) -> None:
        backend = min(self._backends, key=lambda b: self._inflight[b.name])
        self._inflight[backend.name] += 1
        try:
            backend.handle(request_id)
        finally:
            # Ensure counter always decrements even if handle() raises
            self._inflight[backend.name] -= 1

    def add_backend(self, backend: BackendServer) -> None:
        self._backends.append(backend)
        self._inflight[backend.name] = 0

    def remove_backend(self, name: str) -> None:
        self._backends = [b for b in self._backends if b.name != name]
        self._inflight.pop(name, None)
        if not self._backends:
            raise RuntimeError("No backends left!")


# ----------------------------------------------------------------------
# Alternative algorithm: weighted round-robin (static weights)
# ----------------------------------------------------------------------


class WeightedRoundRobinLoadBalancer:
    """Distributes requests proportionally to each backend's weight.

    Weight table is static for the demo; a real impl. would recompute after
    add/remove or allow dynamic weight changes.
    """

    def __init__(self, backends: Iterable[BackendServer], weights: dict[str, int]):
        # Expand the back-end list according to weights, then just round-robin.
        expanded: list[BackendServer] = []
        for b in backends:
            w = max(1, weights.get(b.name, 1))  # default weight 1
            expanded.extend([b] * w)

        if not expanded:
            raise ValueError("No backends available after applying weights")

        self._rr = RoundRobinLoadBalancer(expanded)

    # delegate -----------------------------------------------------------
    def route(self, request_id: int) -> None:  # noqa: D401 – imperative
        self._rr.route(request_id)


# ----------------------------------------------------------------------
# Demo harness
# ----------------------------------------------------------------------

def main() -> None:  # noqa: D401 – imperative demo
    backends = [BackendServer(f"backend-{i}") for i in range(1, 4)]
    lb_rr = RoundRobinLoadBalancer(backends)

    print("=== Round-robin : 6 requests ===")
    for req in range(1, 7):
        lb_rr.route(req)

    # ----- least-connections demo -----
    lb_lc = LeastConnectionsLoadBalancer(backends)

    print("\n=== Least-connections : 6 requests ===")
    for req in range(7, 13):
        lb_lc.route(req)

    print("\n=== Least-connections : add backend-4 ===")
    lb_lc.add_backend(BackendServer("backend-4"))
    for req in range(13, 19):
        lb_lc.route(req)

    print("\n=== Least-connections : remove backend-2 ===")
    lb_lc.remove_backend("backend-2")
    for req in range(19, 25):
        lb_lc.route(req)

    # ----- weighted round-robin demo -----
    print("\n=== Weighted round-robin (backend-1 weight 3, others 1) ===")
    weights = {
        "backend-1": 3,
        "backend-3": 1,
        "backend-4": 1,
    }
    lb_wrr = WeightedRoundRobinLoadBalancer(backends, weights)
    for req in range(25, 37):  # 12 requests; expect ~6 to b1, ~2 each others
        lb_wrr.route(req)


if __name__ == "__main__":
    main() 