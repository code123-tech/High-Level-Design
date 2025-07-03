#!/usr/bin/env python3
"""
scalability_performance_demo.py

Demo: Compare bulk insert performance in SQL (sqlite3) and NoSQL (Python dict).

Inserts 10,000 records into each and measures the time taken.
"""
import sqlite3
import time

N = 10_000

# SQL DEMO (sqlite3)
def sql_bulk_insert():
    print("\n--- SQL (sqlite3) Bulk Insert Performance Demo ---")
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, value TEXT)")
    start = time.time()
    for i in range(N):
        cur.execute("INSERT INTO items (value) VALUES (?)", (f"val-{i}",))
    conn.commit()
    elapsed = time.time() - start
    print(f"Inserted {N} rows in {elapsed:.3f} seconds.")
    conn.close()
    return elapsed

# NoSQL DEMO (Python dict as key-value store)
def nosql_bulk_insert():
    print("\n--- NoSQL (dict) Bulk Insert Performance Demo ---")
    db = {}
    start = time.time()
    for i in range(N):
        db[f"key:{i}"] = {"value": f"val-{i}"}
    elapsed = time.time() - start
    print(f"Inserted {N} documents in {elapsed:.3f} seconds.")
    return elapsed

def main():
    sql_time = sql_bulk_insert()
    nosql_time = nosql_bulk_insert()
    print(f"\nSQL time:   {sql_time:.3f} s\nNoSQL time: {nosql_time:.3f} s")
    print("\n✅  Demo complete. Compare the times to get a sense of bulk insert performance.")

if __name__ == "__main__":
    main() 