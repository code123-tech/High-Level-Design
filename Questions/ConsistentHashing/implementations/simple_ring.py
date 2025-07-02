"""simple_ring.py – minimal consistent hash ring for demo purposes.

Not production-grade; optimised for clarity, not raw speed.
"""
from __future__ import annotations

import bisect
import hashlib
from typing import Dict, List


class ConsistentHashRing:
    """A consistent hash ring with virtual nodes.

    Parameters
    ----------
    virtual_nodes : int
        How many virtual points to assign to each physical node.
    hash_bits : int, optional
        How many bits of the SHA-256 digest to use (default 32) so the ring
        fits into Python ints nicely.
    """

    def __init__(self, virtual_nodes: int = 100, hash_bits: int = 32):
        if virtual_nodes <= 0:
            raise ValueError("virtual_nodes must be > 0")
        self._vn = virtual_nodes
        self._hash_bits = hash_bits
        self._ring: Dict[int, str] = {}
        self._sorted_keys: List[int] = []

    # ──────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────
    def add_node(self, node: str) -> None:
        for i in range(self._vn):
            digest = self._hash(f"{node}#{i}")
            self._ring[digest] = node
            bisect.insort(self._sorted_keys, digest)

    def remove_node(self, node: str) -> None:
        removed = 0
        to_delete = []
        for k in self._sorted_keys:
            if self._ring[k] == node:
                to_delete.append(k)
        for k in to_delete:
            self._sorted_keys.remove(k)
            del self._ring[k]
            removed += 1
        if removed == 0:
            raise ValueError(f"node {node!r} not found on ring")

    def get_node(self, key: str) -> str:
        if not self._ring:
            raise RuntimeError("Ring is empty")
        h = self._hash(key)
        idx = bisect.bisect_left(self._sorted_keys, h)
        if idx == len(self._sorted_keys):
            idx = 0  # wrap around
        digest = self._sorted_keys[idx]
        return self._ring[digest]

    # ──────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────
    def _hash(self, key: str) -> int:
        digest = hashlib.sha256(key.encode("utf-8")).digest()
        # Use the first *hash_bits* of the digest. Max 64 to fit into Python int.
        mask_bytes = self._hash_bits // 8
        val = int.from_bytes(digest[:mask_bytes], "little")
        return val

    # ──────────────────────────────────────────────────────────────────────
    # Debug / stats helpers
    # ──────────────────────────────────────────────────────────────────────
    @property
    def nodes(self):
        return set(self._ring.values())

    def distribution(self, keys: List[str]) -> Dict[str, int]:
        counts: Dict[str, int] = {n: 0 for n in self.nodes}
        for k in keys:
            counts[self.get_node(k)] += 1
        return counts 