from time import time
from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass
class SlidingWindowCounter:
    """
    Sliding Window Counter Rate Limiter Implementation
    
    window_size: size of the window in seconds
    max_requests: maximum number of requests allowed in the window
    """
    window_size: int
    max_requests: int
    
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.current_window: Tuple[int, int] = (0, 0)  # (window_start, count)
        self.previous_window: Tuple[int, int] = (0, 0)  # (window_start, count)
        
    def _update_windows(self) -> None:
        """Update window counters based on current time"""
        current_time = int(time())
        window_start = current_time - (current_time % self.window_size)
        
        # If we're in a new window
        if window_start != self.current_window[0]:
            # If the new window is adjacent to the current window
            if window_start - self.current_window[0] == self.window_size:
                self.previous_window = self.current_window
            else:
                self.previous_window = (0, 0)
            self.current_window = (window_start, 0)
            
    def _calculate_requests(self) -> float:
        """Calculate the weighted request count for the sliding window"""
        current_time = time()
        window_start = self.current_window[0]
        
        # Calculate the position in the current window (0 to 1)
        position = (current_time - window_start) / self.window_size
        
        # Weight the previous window's count based on position
        previous_count = self.previous_window[1] * (1 - position)
        
        # Add the current window's count
        return previous_count + self.current_window[1]
        
    def allow_request(self) -> bool:
        """
        Check if request can be allowed
        Returns True if request is allowed, False otherwise
        """
        self._update_windows()
        
        # Check if we've exceeded the limit
        if self._calculate_requests() >= self.max_requests:
            return False
            
        # Increment counter and allow request
        self.current_window = (self.current_window[0], self.current_window[1] + 1)
        return True
        
    def get_remaining_quota(self) -> int:
        """Get remaining requests allowed in current window"""
        self._update_windows()
        current_requests = self._calculate_requests()
        return max(0, int(self.max_requests - current_requests))

class RateLimiter:
    """Rate limiter that manages multiple sliding window counters"""
    def __init__(self):
        self.limiters: Dict[str, SlidingWindowCounter] = {}
        
    def add_limiter(self, key: str, window_size: int, max_requests: int) -> None:
        """Add a new rate limiter for a specific key"""
        self.limiters[key] = SlidingWindowCounter(window_size, max_requests)
        
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
    
    # Add limiter: 10 requests per 60 second sliding window
    limiter.add_limiter("api/users", window_size=60, max_requests=10)
    
    # Simulate requests with timestamps
    from time import sleep
    
    print("Simulating requests over 2 minutes...")
    for i in range(15):
        if limiter.is_allowed("api/users"):
            print(f"[{time():.1f}] Request {i} allowed "
                  f"(remaining: {limiter.get_remaining_quota('api/users')})")
        else:
            print(f"[{time():.1f}] Request {i} blocked "
                  f"(remaining: {limiter.get_remaining_quota('api/users')})")
        sleep(10)  # Wait 10 seconds between requests

if __name__ == "__main__":
    example_usage() 