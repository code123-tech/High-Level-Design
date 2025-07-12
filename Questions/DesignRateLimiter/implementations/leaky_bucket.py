from collections import deque
from time import time, sleep
from threading import Thread, Lock
from typing import Dict

class LeakyBucket:
    """
    Leaky Bucket Rate Limiter Implementation
    
    capacity: maximum number of requests that can be queued
    leak_rate: number of requests processed per second
    """
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.bucket = deque()
        self.lock = Lock()
        self.running = True
        
        # Start processor thread
        self.processor = Thread(target=self._process_requests)
        self.processor.daemon = True
        self.processor.start()
        
    def add_request(self) -> bool:
        """
        Try to add a request to the bucket
        Returns True if request is accepted, False if rejected
        """
        with self.lock:
            if len(self.bucket) < self.capacity:
                self.bucket.append(time())
                return True
            return False
            
    def _process_requests(self) -> None:
        """Process requests at the specified leak rate"""
        while self.running:
            with self.lock:
                if self.bucket:
                    self.bucket.popleft()
            sleep(1 / self.leak_rate)
            
    def stop(self) -> None:
        """Stop the request processor"""
        self.running = False
        self.processor.join()

class RateLimiter:
    """Rate limiter that manages multiple leaky buckets"""
    def __init__(self):
        self.limiters: Dict[str, LeakyBucket] = {}
        
    def add_limiter(self, key: str, capacity: int, leak_rate: float) -> None:
        """Add a new rate limiter for a specific key"""
        self.limiters[key] = LeakyBucket(capacity, leak_rate)
        
    def is_allowed(self, key: str) -> bool:
        """Check if request for given key is allowed"""
        if key not in self.limiters:
            return False
        return self.limiters[key].add_request()
        
    def stop_all(self) -> None:
        """Stop all limiters"""
        for limiter in self.limiters.values():
            limiter.stop()

def example_usage():
    # Create rate limiter
    limiter = RateLimiter()
    
    try:
        # Add limiters for different API endpoints
        limiter.add_limiter("api/users", 5, 2)  # 5 requests queue, 2 requests/second
        limiter.add_limiter("api/orders", 3, 1) # 3 requests queue, 1 request/second
        
        # Simulate burst of requests
        for i in range(10):
            if limiter.is_allowed("api/users"):
                print(f"Request {i} to /users queued")
            else:
                print(f"Request {i} to /users rejected (queue full)")
            sleep(0.1)  # Small delay between requests
            
    finally:
        # Ensure limiters are stopped properly
        limiter.stop_all()

if __name__ == "__main__":
    example_usage() 