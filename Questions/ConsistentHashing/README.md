# Consistent Hashing – Learning Module

This folder complements the conceptual notes in
[`../../BasicConcepts/Consistent_Hashing.md`](../../BasicConcepts/Consistent_Hashing.md)
with **runnable demos** and **hands-on experiments**.

> Why duplicate the concept here?  Because nothing beats _seeing_ how keys
> redistribute, or _measuring_ the impact of virtual nodes, replication, and
> node churn on load-balance.

---

## Folder layout

```
ConsistentHashing/
├── ConsistentHashing.java        # Minimal Java implementation (existing)
├── ConsistentHashingDemo.java    # Java demo (existing)
├── quick_start.py                # Interactive launcher (new)
├── implementations/              # Python reference ring + demos
│   ├── simple_ring.py            # Lightweight consistent-hash ring class
│   └── load_distribution_demo.py # First demo – key distribution histogram
└── README.md                     # This file
```

## Quick start

```bash
# From project root
python Questions/ConsistentHashing/quick_start.py
```

Inside the launcher you can:
1. Run the **Load-distribution demo** (shows how evenly keys spread).
2. (Coming soon) Replication & node-removal demo.
3. Explore the file structure.

Feel free to extend the **implementations/** folder with more demos – the
menu will automatically detect new scripts.

## Learning objectives

* Understand how virtual nodes improve balance.
* Visualise what happens when a node joins or leaves.
* Compare ring-hash with jump consistent hash (exercise stub).
* Measure standard-deviation of key counts across servers.

Have fun poking the ring! ✨ 