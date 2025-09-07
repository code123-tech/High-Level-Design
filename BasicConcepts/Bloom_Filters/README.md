## Table of Contents
1. [Introduction](#introduction)
2. [How Bloom Filters Work](#how-bloom-filters-work)
3. [Tuning and Trade-offs](#tuning-and-trade-offs)
4. [Where They Shine (Use Cases)](#where-they-shine-use-cases)
5. [When Not To Use](#when-not-to-use)
6. [References](#references)

## Introduction
- Definition: A Bloom filter is a tiny, probabilistic set that answers: "Have I probably seen this item before?" It can say "maybe" for membership (allowing a small false-positive rate) but will never say "no" if the item was actually inserted (no false negatives).

- Why you should care:
    - It saves memory dramatically versus storing full sets.
    - It keeps performance predictable: O(k) time per insert/lookup, where k is small (number of hash functions).
    - It prevents expensive downstream work (e.g., skipping disk/db lookups for items that are surely not present).

- Mental model:
    - Imagine a compact array of bits, all zeros at start. Each item you insert flips k bit positions to 1. To query, you check those same k positions. If any is 0 → definitely not present. If all are 1 → probably present.

## How Bloom Filters Work
- Data structure:
    - A bit array of size m.
    - k independent hash functions mapping an element to k indices in [0, m).

- Insert(x):
    - Compute k hashes: h1(x), h2(x), ..., hk(x).
    - Set bits at those positions to 1.

- MightContain(x):
    - Compute the same k hashes.
    - If any bit is 0 → definitely NOT present.
    - If all bits are 1 → PROBABLY present (could be a false positive).

- No deletes (in the vanilla version):
    - Standard Bloom filters do not support removal. A variant called "Counting Bloom Filter" uses small counters instead of bits to allow decrement on delete (at extra memory cost).

## Tuning and Trade-offs
- Misinformation budget = false positive rate (FPR):
    - Target FPR (e.g., 1%) dictates the needed bit array size m and number of hashes k for n expected items.
    - Optimal k ≈ (m/n) ln 2; and FPR ≈ (1 - e^{-kn/m})^k.

- Picking parameters:
    - Given n items and target FPR p, you can solve for m and k:
        - m ≈ - (n ln p) / (ln 2)^2
        - k ≈ (m/n) ln 2
    - Many libraries compute these for you; you just provide n and p.

- Space vs accuracy:
    - More bits (m) → lower FPR but more memory.
    - More hashes (k) → lower FPR but slower inserts/lookups. In practice k is small (e.g., 4–10).

- Scaling and saturation:
    - If you insert far more than n, the filter saturates (too many 1s) and FPR rises sharply. Rebuild with larger m when you outgrow it.

## Where They Shine (Use Cases)
- Cache miss filters: Avoid asking the database for keys that definitely aren’t present.
- Web crawlers: Skip re-fetching URLs already seen.
- Mail systems: Pre-filter spam signatures before heavier checks.
- Distributed systems: Reduce network chatter by screening requests (e.g., Bigtable/HBase SSTable lookups).
- Security/privacy: Quick membership checks for leaked-password sets (with care for side-channels).

## When Not To Use
- You need exact answers (no false positives tolerated).
- You need deletions without extra overhead (use Counting Bloom Filters if necessary).
- The dataset is tiny and simplicity matters more than memory savings.

## References
- Blogs: `https://llimllib.github.io/bloomfilter-tutorial/`
- Paper: Burton H. Bloom, "Space/Time Trade-offs in Hash Coding with Allowable Errors" (1970)
- Libraries:
    - Java: Guava `BloomFilter`
    - Go: `willf/bloom`
    - Python: `pybloom` / `bloom-filter`

