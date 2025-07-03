#!/usr/bin/env python3
"""
transaction_consistency_demo.py

Demo: Compare transaction consistency in SQL (sqlite3, ACID) and NoSQL (Python dict, eventual consistency simulation).

Shows how atomic transactions work in SQL and how eventual consistency might look in a NoSQL-like system.
"""
import sqlite3
import time

# SQL DEMO (sqlite3)
def sql_transaction_demo():
    print("\n--- SQL (sqlite3) Transaction Consistency Demo ---")
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")
    cur.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", ("Alice", 100))
    cur.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", ("Bob", 100))
    conn.commit()
    print("Initial balances:")
    cur.execute("SELECT name, balance FROM accounts")
    print(cur.fetchall())
    # Begin transaction: transfer 50 from Alice to Bob
    try:
        cur.execute("BEGIN TRANSACTION")
        cur.execute("UPDATE accounts SET balance = balance - 50 WHERE name = ?", ("Alice",))
        # Uncomment the next line to simulate a failure:
        # raise Exception("Simulated failure!")
        cur.execute("UPDATE accounts SET balance = balance + 50 WHERE name = ?", ("Bob",))
        conn.commit()
        print("\nAfter transaction (transfer 50 from Alice to Bob):")
    except Exception as e:
        conn.rollback()
        print("\nTransaction failed, rolled back:", e)
    cur.execute("SELECT name, balance FROM accounts")
    print(cur.fetchall())
    conn.close()

# NoSQL DEMO (Python dict, eventual consistency simulation)
def nosql_eventual_consistency_demo():
    print("\n--- NoSQL (dict) Eventual Consistency Demo ---")
    # Simulate two replicas
    replica1 = {"Alice": 100, "Bob": 100}
    replica2 = {"Alice": 100, "Bob": 100}
    print("Initial balances (replica1, replica2):", replica1, replica2)
    # Simulate a write to replica1 only (network partition)
    print("\nSimulating network partition: updating Alice's balance on replica1 only...")
    replica1["Alice"] -= 50
    replica1["Bob"] += 50
    print("Balances after write (replica1, replica2):", replica1, replica2)
    # After some time, replicas sync (eventual consistency)
    print("\nSynchronizing replicas (eventual consistency)...")
    time.sleep(1)
    replica2 = replica1.copy()
    print("Balances after sync (replica1, replica2):", replica1, replica2)


def main():
    sql_transaction_demo()
    nosql_eventual_consistency_demo()
    print("\n✅  Demo complete. Notice the difference between ACID transaction and eventual consistency.")

if __name__ == "__main__":
    main() 