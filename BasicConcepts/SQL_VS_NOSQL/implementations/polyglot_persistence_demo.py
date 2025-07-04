#!/usr/bin/env python3
"""
polyglot_persistence_demo.py

Demo: Polyglot Persistence – Using SQL for user profiles and NoSQL for logs.

- Writes user profiles to SQL (sqlite3).
- Writes user logs to a NoSQL (Python list of dicts).
- Shows how both can be queried together for analytics (e.g., join user info with log counts).

This script is for learning purposes and does not require any external database.
"""
import sqlite3
from collections import Counter

# Step 1: Write user profiles to SQL
def write_user_profiles():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    users = [
        (1, "Alice", "alice@example.com"),
        (2, "Bob", "bob@example.com"),
        (3, "Carol", "carol@example.com"),
    ]
    cur.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
    conn.commit()
    return conn

# Step 2: Write logs to NoSQL (list of dicts)
def write_user_logs():
    logs = [
        {"user_id": 1, "action": "login"},
        {"user_id": 1, "action": "view"},
        {"user_id": 2, "action": "login"},
        {"user_id": 2, "action": "purchase"},
        {"user_id": 3, "action": "login"},
        {"user_id": 1, "action": "logout"},
    ]
    return logs

# Step 3: Analytics – join SQL and NoSQL data
def analytics(conn, logs):
    print("\n--- Polyglot Analytics: User Profiles + Log Counts ---")
    cur = conn.cursor()
    # Count logs per user
    log_counts = Counter(log["user_id"] for log in logs)
    # Query user info and join with log counts
    cur.execute("SELECT id, name, email FROM users")
    for user_id, name, email in cur.fetchall():
        count = log_counts.get(user_id, 0)
        print(f"User: {name:5} | Email: {email:20} | Log entries: {count}")

    print("\nSample: List all actions for Alice:")
    alice_logs = [log["action"] for log in logs if log["user_id"] == 1]
    print(f"Alice's actions: {alice_logs}")


def main():
    conn = write_user_profiles()
    logs = write_user_logs()
    analytics(conn, logs)
    print("\n✅  Demo complete. This shows how SQL and NoSQL can be used together for richer analytics (polyglot persistence).")

if __name__ == "__main__":
    main() 