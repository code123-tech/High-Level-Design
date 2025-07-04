import streamlit as st
import sqlite3
import json
from copy import deepcopy

st.set_page_config(page_title="Interactive Web Playground", layout="wide")

st.title("🧑‍💻 Interactive Web Playground: SQL & NoSQL")
st.write("Experiment with SQL (SQLite) and NoSQL (MongoDB-style) queries live!")

# --- Example Data ---
SQL_EXAMPLE = """-- Try:
SELECT * FROM users;
INSERT INTO users (name, age) VALUES ('Dave', 40);
UPDATE users SET age = 29 WHERE name = 'Alice';
DELETE FROM users WHERE name = 'Bob';
"""
NOSQL_EXAMPLE = """# Try:
{"name": "Alice"}
{"age": {"$gt": 25}}
{}  # all users
"""

# --- Sidebar for playground selection ---
playground = st.sidebar.radio(
    "Choose Playground:",
    ("SQL (SQLite)", "NoSQL (MongoDB-style)")
)

# --- SQL Playground ---
def init_sqlite_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)")
    cur.executemany(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        [("Alice", 28), ("Bob", 35), ("Carol", 22)]
    )
    conn.commit()
    return conn

def run_sql_query(conn, query):
    cur = conn.cursor()
    try:
        cur.execute(query)
        if query.strip().lower().startswith("select"):
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return {"columns": columns, "rows": rows, "error": None, "is_select": True}
        else:
            conn.commit()
            return {"columns": [], "rows": [], "error": None, "is_select": False, "message": "Query executed successfully."}
    except Exception as e:
        return {"columns": [], "rows": [], "error": str(e), "is_select": query.strip().lower().startswith("select")}

def show_sql_table(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        if rows:
            st.dataframe(
                {col: [row[i] for row in rows] for i, col in enumerate(columns)},
                use_container_width=True
            )
        else:
            st.info("No results.")
    except Exception as e:
        st.error(f"Error displaying table: {e}")

# --- NoSQL Playground ---
NOSQL_SAMPLE = [
    {"name": "Alice", "age": 28, "city": "London"},
    {"name": "Bob", "age": 35, "city": "Paris"},
    {"name": "Carol", "age": 22, "city": "Berlin"},
]

def nosql_find(collection, query):
    # Only support simple equality and $gt/$lt for demo
    def match(doc, q):
        for k, v in q.items():
            if isinstance(v, dict):
                # Support $gt/$lt
                for op, val in v.items():
                    if op == "$gt" and not (doc.get(k, None) is not None and doc[k] > val):
                        return False
                    if op == "$lt" and not (doc.get(k, None) is not None and doc[k] < val):
                        return False
            else:
                if doc.get(k) != v:
                    return False
        return True
    return [doc for doc in collection if match(doc, query)]

# --- Main UI Logic ---
if playground == "SQL (SQLite)":
    st.header("SQL Playground (SQLite)")
    st.write("Enter your SQL query below:")
    sql_query = st.text_area("SQL Query", SQL_EXAMPLE, height=150)
    if st.button("Run SQL Query"):
        conn = init_sqlite_db()
        result = run_sql_query(conn, sql_query)
        if result["error"]:
            st.error(f"Error: {result['error']}")
        elif result["is_select"]:
            if result["rows"]:
                st.dataframe(
                    {col: [row[i] for row in result["rows"]] for i, col in enumerate(result["columns"])},
                    use_container_width=True
                )
            else:
                st.info("No results.")
        else:
            st.success(result["message"])
            st.write("Current contents of 'users' table:")
            show_sql_table(conn)

elif playground == "NoSQL (MongoDB-style)":
    st.header("NoSQL Playground (MongoDB-style)")
    st.write("Enter your NoSQL query (as Python dict or JSON) below:")
    nosql_query = st.text_area("NoSQL Query", NOSQL_EXAMPLE, height=150)
    if st.button("Run NoSQL Query"):
        try:
            # Accept both Python dict and JSON
            query = eval(nosql_query, {"__builtins__": {}})
            if not isinstance(query, dict):
                raise ValueError("Query must be a dict.")
            results = nosql_find(deepcopy(NOSQL_SAMPLE), query)
            if results:
                st.dataframe(results, use_container_width=True)
            else:
                st.info("No matching documents.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.caption("Supported: equality, $gt, $lt. Example: {'age': {'$gt': 25}} or {'name': 'Alice'}") 