#!/usr/bin/env python3
"""
join_vs_aggregation_demo.py

Demo: Compare SQL JOIN (sqlite3) with NoSQL aggregation (MongoDB-style pipeline and Redis-style application-side join).

- SQL: Perform a JOIN between two tables.
- NoSQL: Show how to achieve the same result using a MongoDB-like aggregation pipeline (in Python) and a Redis-like application-side join.

This script is for learning purposes and does not require any external database.
"""
import sqlite3
from pprint import pprint

# SQL DEMO (sqlite3 JOIN)
def sql_join_demo():
    print("\n--- SQL (sqlite3) JOIN Demo ---")
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    # Create tables
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, product TEXT)")
    # Insert data
    cur.executemany("INSERT INTO users (name) VALUES (?)", [("Alice",), ("Bob",)])
    cur.executemany("INSERT INTO orders (user_id, product) VALUES (?, ?)", [(1, "Book"), (1, "Pen"), (2, "Notebook")])
    conn.commit()
    # JOIN query: Get all users and their orders
    cur.execute("""
        SELECT users.name, orders.product
        FROM users
        JOIN orders ON users.id = orders.user_id
    """)
    print("User Orders (via JOIN):")
    for row in cur.fetchall():
        print(row)
    conn.close()

# NoSQL DEMO (MongoDB-style aggregation pipeline)
def nosql_mongodb_aggregation_demo():
    print("\n--- NoSQL (MongoDB-style Aggregation) Demo ---")
    users = [
        {"_id": 1, "name": "Alice"},
        {"_id": 2, "name": "Bob"},
    ]
    orders = [
        {"_id": 1, "user_id": 1, "product": "Book"},
        {"_id": 2, "user_id": 1, "product": "Pen"},
        {"_id": 3, "user_id": 2, "product": "Notebook"},
    ]
    # Simulate $lookup (join) in aggregation pipeline
    result = []
    for user in users:
        user_orders = [order["product"] for order in orders if order["user_id"] == user["_id"]]
        result.append({"name": user["name"], "orders": user_orders})
    print("User Orders (via aggregation/$lookup):")
    pprint(result)

# NoSQL DEMO (Redis-style application-side join)
def nosql_redis_app_side_join_demo():
    print("\n--- NoSQL (Redis-style Application-side Join) Demo ---")
    # Simulate Redis as two key-value stores
    users = {
        1: {"name": "Alice"},
        2: {"name": "Bob"},
    }
    orders = {
        1: {"user_id": 1, "product": "Book"},
        2: {"user_id": 1, "product": "Pen"},
        3: {"user_id": 2, "product": "Notebook"},
    }
    # Application-side join: for each user, find their orders
    for user_id, user in users.items():
        user_orders = [order["product"] for order in orders.values() if order["user_id"] == user_id]
        print(f"{user['name']} orders: {user_orders}")

def main():
    sql_join_demo()
    nosql_mongodb_aggregation_demo()
    nosql_redis_app_side_join_demo()
    print("\n✅  Demo complete. Notice how SQL handles joins natively, while NoSQL often requires aggregation pipelines or application-side logic.")

if __name__ == "__main__":
    main() 