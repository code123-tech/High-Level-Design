from time import time
from typing import Dict, Tuple

class FixedWindowCounter:
    """
    Fixed Window Counter Rate Limiter Implementation
    
    window_size: size of the window in seconds
    max_requests: maximum number of requests allowed in the window
    """
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.current_window: Tuple[int, int] = (0, 0)  # (window_start, count)
        
    def allow_request(self) -> bool:
        """
        Check if request can be allowed
        Returns True if request is allowed, False otherwise
        """
        current_time = int(time())
        window_start = current_time - (current_time % self.window_size)
        
        # If we're in a new window, reset the counter
        if window_start != self.current_window[0]:
            self.current_window = (window_start, 0)
            
        # Check if we've exceeded the limit
        if self.current_window[1] >= self.max_requests:
            return False
            
        # Increment counter and allow request
        self.current_window = (window_start, self.current_window[1] + 1)
        return True
        
    def get_remaining_quota(self) -> int:
        """Get remaining requests allowed in current window"""
        current_time = int(time())
        window_start = current_time - (current_time % self.window_size)
        
        # If we're in a new window, return full quota
        if window_start != self.current_window[0]:
            return self.max_requests
            
        return max(0, self.max_requests - self.current_window[1])

class RateLimiter:
    """Rate limiter that manages multiple fixed window counters"""
    def __init__(self):
        self.limiters: Dict[str, FixedWindowCounter] = {}
        
    def add_limiter(self, key: str, window_size: int, max_requests: int) -> None:
        """Add a new rate limiter for a specific key"""
        self.limiters[key] = FixedWindowCounter(window_size, max_requests)
        
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
    # 100 requests per 60 second window
    limiter.add_limiter("api/users", window_size=60, max_requests=100)
    # 50 requests per 30 second window
    limiter.add_limiter("api/orders", window_size=30, max_requests=50)
    
    # Simulate requests
    for i in range(120):
        if limiter.is_allowed("api/users"):
            print(f"Request {i} to /users allowed "
                  f"(remaining: {limiter.get_remaining_quota('api/users')})")
        else:
            print(f"Request {i} to /users blocked "
                  f"(remaining: {limiter.get_remaining_quota('api/users')})")

if __name__ == "__main__":
    example_usage() 