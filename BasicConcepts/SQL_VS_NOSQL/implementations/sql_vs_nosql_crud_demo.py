#!/usr/bin/env python3
"""
sql_vs_nosql_crud_demo.py

Demo: Compare basic CRUD operations in SQL (sqlite3) and NoSQL (Python dict).

This script is for learning purposes and does not require any external database.
"""
import sqlite3

# SQL DEMO (sqlite3)
def sql_demo():
    print("\n--- SQL (sqlite3) CRUD Demo ---")
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    # Create
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
    conn.commit()
    # Read
    cur.execute("SELECT * FROM users")
    print("Users:", cur.fetchall())
    # Update
    cur.execute("UPDATE users SET age = ? WHERE name = ?", (31, "Alice"))
    conn.commit()
    cur.execute("SELECT * FROM users WHERE name = ?", ("Alice",))
    print("Updated Alice:", cur.fetchone())
    # Delete
    cur.execute("DELETE FROM users WHERE name = ?", ("Bob",))
    conn.commit()
    cur.execute("SELECT * FROM users")
    print("After deleting Bob:", cur.fetchall())
    conn.close()

# NoSQL DEMO (Python dict as key-value/document store)
def nosql_demo():
    print("\n--- NoSQL (dict) CRUD Demo ---")
    db = {}
    # Create
    db["user:1"] = {"name": "Alice", "age": 30}
    db["user:2"] = {"name": "Bob", "age": 25}
    # Read
    print("Users:", list(db.values()))
    # Update
    db["user:1"]["age"] = 31
    print("Updated Alice:", db["user:1"])
    # Delete
    del db["user:2"]
    print("After deleting Bob:", list(db.values()))

def main():
    sql_demo()
    nosql_demo()
    print("\n✅  Demo complete. Compare the output and notice the differences in syntax and data model.")

if __name__ == "__main__":
    main() 