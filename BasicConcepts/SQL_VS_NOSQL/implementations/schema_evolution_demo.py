#!/usr/bin/env python3
"""
schema_evolution_demo.py

Demo: Compare schema evolution in SQL (sqlite3) and NoSQL (Python dict as document store).

Shows how adding a new field/column is handled in each system.
"""
import sqlite3

# SQL DEMO (sqlite3)
def sql_schema_evolution():
    print("\n--- SQL (sqlite3) Schema Evolution Demo ---")
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
    conn.commit()
    print("Initial table:")
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    # Add a new column (age)
    print("\nAltering table to add 'age' column...")
    cur.execute("ALTER TABLE users ADD COLUMN age INTEGER")
    # Update Alice's age
    cur.execute("UPDATE users SET age = ? WHERE name = ?", (30, "Alice"))
    conn.commit()
    print("Table after schema change and update:")
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
    conn.close()

# NoSQL DEMO (Python dict as document store)
def nosql_schema_evolution():
    print("\n--- NoSQL (dict) Schema Evolution Demo ---")
    db = {}
    db["user:1"] = {"name": "Alice"}
    db["user:2"] = {"name": "Bob"}
    print("Initial documents:")
    print(list(db.values()))
    # Add a new field (age) to Alice
    db["user:1"]["age"] = 30
    print("\nAfter adding 'age' field to Alice:")
    print(list(db.values()))


def main():
    sql_schema_evolution()
    nosql_schema_evolution()
    print("\n✅  Demo complete. Notice the difference in how schema changes are handled.")

if __name__ == "__main__":
    main() 