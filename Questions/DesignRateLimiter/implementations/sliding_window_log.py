from time import time
from typing import Dict, List
from collections import deque
from dataclasses import dataclass, field

@dataclass
class SlidingWindowLog:
    """
    Sliding Window Log Rate Limiter Implementation
    
    window_size: size of the window in seconds
    max_requests: maximum number of requests allowed in the window
    """
    window_size: int
    max_requests: int
    requests: deque = field(default_factory=lambda: deque())
    
    def _cleanup_old_requests(self) -> None:
        """Remove requests outside the current window"""
        now = time()
        while self.requests and self.requests[0] <= now - self.window_size:
            self.requests.popleft()
            
    def allow_request(self) -> bool:
        """
        Check if request can be allowed
        Returns True if request is allowed, False otherwise
        """
        now = time()
        self._cleanup_old_requests()
        
        # Check if we've exceeded the limit
        if len(self.requests) >= self.max_requests:
            return False
            
        # Add current request timestamp
        self.requests.append(now)
        return True
        
    def get_remaining_quota(self) -> int:
        """Get remaining requests allowed in current window"""
        self._cleanup_old_requests()
        return max(0, self.max_requests - len(self.requests))

class RateLimiter:
    """Rate limiter that manages multiple sliding window logs"""
    def __init__(self):
        self.limiters: Dict[str, SlidingWindowLog] = {}
        
    def add_limiter(self, key: str, window_size: int, max_requests: int) -> None:
        """Add a new rate limiter for a specific key"""
        self.limiters[key] = SlidingWindowLog(window_size, max_requests)
        
    def is_allowed(self, key: str) -> bool:
        """Check if request for given key is allowed"""
        if key not in self.limiters:
            return False
        return self.limiters[key].allow_request()
        
    def get_remaining_quota(self, key: str) -> int:
        """Get remaining quota for given key"""
        if key not in self.limiters:
            return 0
        return self.limiters[key].get_remaining_quota()

def example_usage():
    # Create rate limiter
    limiter = RateLimiter()
    
    # Add limiters for different API endpoints
    # 5 requests per 10 second sliding window
    limiter.add_limiter("api/users", window_size=10, max_requests=5)
    
    # Simulate requests with timestamps
    from time import sleep
    
    print("Simulating requests over 15 seconds...")
    for i in range(8):
        if limiter.is_allowed("api/users"):
            print(f"[{time():.1f}] Request {i} allowed "
                  f"(remaining: {limiter.get_remaining_quota('api/users')})")
        else:
            print(f"[{time():.1f}] Request {i} blocked "
                  f"(remaining: {limiter.get_remaining_quota('api/users')})")
        sleep(2)  # Wait 2 seconds between requests

if __name__ == "__main__":
    example_usage() 