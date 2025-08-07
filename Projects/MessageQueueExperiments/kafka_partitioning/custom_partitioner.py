from typing import Any
from kafka.partitioner.default import DefaultPartitioner

class RoundRobinPartitioner(DefaultPartitioner):
    """Custom partitioner that implements round-robin strategy"""
    def __init__(self):
        super().__init__()
        self._counter = 0

    def partition(self, topic: str, key: Any, all_partitions: list, available: list) -> int:
        if not available:
            return self._random(all_partitions)
        
        num_partitions = len(available)
        chosen_partition = available[self._counter % num_partitions].id
        self._counter += 1
        return chosen_partition

class KeyBasedPartitioner(DefaultPartitioner):
    """Custom partitioner that uses key hash for consistent message routing"""
    def partition(self, topic: str, key: Any, all_partitions: list, available: list) -> int:
        if not key or not available:
            return self._random(all_partitions)
        
        # Use key hash to determine partition
        key_bytes = str(key).encode('utf-8')
        key_hash = sum(key_bytes)
        num_partitions = len(available)
        return available[key_hash % num_partitions].id
