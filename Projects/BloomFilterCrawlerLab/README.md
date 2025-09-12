### Design notes (Why these choices?)

- **Why `(m + 7) // 8` for allocation?**
  - The Bloom filter tracks `m` bits, but memory is addressed in bytes. We need `ceil(m/8)` bytes to store `m` bits. The expression `(m + 7) // 8` is integer ceil-division of `m/8`.
  - Example: if `m = 10` bits → `(10 + 7) // 8 = 2` bytes (16 bits), enough to cover all 10 bit positions.

- **Why `bytearray` instead of an array/list of 0/1?**
  - **Memory efficiency**: `bytearray` packs 8 bits per byte; a list/array of ints stores at least 1 byte per flag (lists are far larger: each element is a Python object). For large `m`, packing bits is critical.
  - **Speed and cache locality**: A compact contiguous `bytearray` fits better in CPU caches than a list of Python objects, improving bit operations.
  - **Simple bit ops**: Set/check via bit masks is fast and idiomatic:
    - `byte_index = idx // 8`, `mask = 1 << (idx % 8)`
    - set: `bits[byte_index] |= mask`
    - check: `(bits[byte_index] & mask) != 0`
  - **Easy serialization**: Convert directly to `bytes` for snapshots and back with minimal overhead.
  - Alternatives like `array('b')` still store per-byte (8× the space of a bitset). Third‑party bitset libs work too but add dependencies; `bytearray` keeps it standard-library only.

- **Deterministic hashing (context)**
  - We generate `k` indices using double hashing: `index(i) = (h1 + i*h2) % m`. In Python, use stable digests (e.g., SHA‑256/SHA‑1) rather than the built‑in `hash()` which is salted per process.
