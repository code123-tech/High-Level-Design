import math, hashlib, struct

'''
We are following the standard bit manipulation techniques here in the code,

- **Why `bytearray` instead of an array/list of 0/1?**
  - **Memory efficiency**: `bytearray` packs 8 bits per byte; a list/array of ints stores at least 1 byte per 
    flag (lists are far larger: each element is a Python object). For large `m`, packing bits is critical.
  - **Speed and cache locality**: A compact contiguous `bytearray` fits better in CPU caches than a list of Python 
     objects, improving bit operations.
  - **Simple bit ops**: Set/check via bit masks is fast and idiomatic:
    - `byte_index = idx // 8`, `mask = 1 << (idx % 8)`
    - set: `bits[byte_index] |= mask`
    - check: `(bits[byte_index] & mask) != 0`
  - **Easy serialization**: Convert directly to `bytes` for snapshots and back with minimal overhead.
  - Alternatives like `array('b')` still store per-byte (8× the space of a bitset). Third‑party bitset libs work too 
    but add dependencies; `bytearray` keeps it standard-library only.
'''

class BloomFilter:

    '''
    - The Bloom filter tracks `m` bits, but memory is addressed in bytes. We need `ceil(m/8)` bytes to store `m` bits. 
      The expression `(m + 7) // 8` is integer ceil-division of `m/8`.
    - Example: if `m = 10` bits → `(10 + 7) // 8 = 2` bytes (16 bits), enough to cover all 10 bit positions.
    '''
    def __init__(self, n, fpr):

        if n <= 0:
            raise ValueError("n must be greater than 0")
        
        if not (0.0 < fpr < 1.0):
            raise ValueError("fpr must be between 0.0 and 1.0")
        
        m = math.ceil(-(n * math.log(fpr)) / (math.log(2) ** 2))
        k = max(1, round((m / n) * math.log(2)))
        
        self.m = m
        self.k = k
        self.bits = bytearray( ( m + 7 ) // 8 )
    

    '''
    - We generate `k` indices using double hashing: `index(i) = (h1 + i*h2) % m`. In Python, use stable 
      digests (e.g., SHA‑256/SHA‑1) rather than the built‑in `hash()` which is salted per process.
    '''
    def _indexes(self, key: str):
        bytes_array = key.encode('utf-8')
        h1 = int.from_bytes(hashlib.sha256(bytes_array).digest()[:8], 'big', signed=False)
        h2 = int.from_bytes(hashlib.sha1(bytes_array).digest()[:8], 'big', signed=False) or 1

        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add_item(self, key: str):

        for index in self._indexes(key):
            self.bits[index // 8] |= (1 << (index % 8))
    
    def check_item_exist(self, key: str):

        for index in self._indexes(key):
            isExist = self.bits[index // 8] & (1 << (index % 8))
            if not isExist:
                return False
        
        return True
    
    
    def serialize(self) -> bytes:
        header = struct.pack('>II', self.m, self.k)
        return header + bytes(self.bits)
    
    @staticmethod
    def deserialize(data: bytes) -> 'BloomFilter':
        m, k = struct.unpack('>II', data[:8])
        bf = object.__new__(BloomFilter)
        bf.m, bf.k = m, k
        bf.bits = bytearray(data[8:])
        return bf
    
    '''
    - returns percent of 1-bits in the filter (saturation). 
    - Used to monitor health and trigger early rotation.
    '''
    def bits_set_percent(self) -> float:
        return self._calculate_ones() * 100.0
    

    def _calculate_ones(self):
        ones = sum(bin(byte).count('1') for byte in self.bits)
        return ones / self.m
    
    '''
    - Estimates current false positive rate from saturation. Uses p0 ≈ 1 − (ones/m), so FPR ≈ (1 − p0)^k
    '''
    def estimate_fpr(self) -> float:
        p1 = 1.0 - self._calculate_ones()
        return (1.0 - p1) ** self.k
