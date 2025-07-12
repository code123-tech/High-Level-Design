from time import time
from dataclasses import dataclass
from typing import Dict

@dataclass
class TokenBucket:
    """
    Token Bucket Rate Limiter Implementation
    
    capacity: maximum number of tokens the bucket can hold
    refill_rate: number of tokens added per second
    """
    capacity: int
    refill_rate: float
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time()
        
    def _refill(self) -> None:
        """Refill tokens based on elapsed time"""
        now = time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now
        
    def allow_request(self) -> bool:
        """
        Check if request can be allowed
        Returns True if request is allowed, False otherwise
        """
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class RateLimiter:
    """Rate limiter that manages multiple token buckets"""
    def __init__(self):
        self.limiters: Dict[str, TokenBucket] = {}
        
    def add_limiter(self, key: str, capacity: int, refill_rate: float) -> None:
        """Add a new rate limiter for a specific key"""
        self.limiters[key] = TokenBucket(capacity, refill_rate)
        
    def is_allowed(self, key: str) -> bool:
        """Check if request for given key is allowed"""
        if key not in self.limiters:
            return False
        return self.limiters[key].allow_request()

def example_usage():
    # Create rate limiter
    limiter = RateLimiter()
    
    # Add limiters for different API endpoints
    limiter.add_limiter("api/users", 100, 10)  # 100 requests capacity, 10 requests/second
    limiter.add_limiter("api/orders", 50, 5)   # 50 requests capacity, 5 requests/second
    
    # Simulate requests
    for _ in range(120):
        if limiter.is_allowed("api/users"):
            print("Request to /users allowed")
        else:
            print("Request to /users blocked (rate limit exceeded)")
            
if __name__ == "__main__":
    example_usage() 