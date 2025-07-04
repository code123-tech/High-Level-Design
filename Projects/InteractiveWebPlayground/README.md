# Interactive Web Playground

This project provides an interactive web-based playground for experimenting with SQL (SQLite) and NoSQL (simulated MongoDB) queries live in your browser.

**Goal:**
- Lower the barrier to experimentation and learning by letting users try queries and see results instantly.

**Features:**
- Enter and run SQL queries (SQLite, in-memory)
- Enter and run NoSQL queries (simulated MongoDB, in-memory)
- See results and errors live
- Example queries provided for both modes

## Setup

1. Make sure you have Python 3.7 or newer installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Your browser will open automatically. Use the sidebar to select SQL or NoSQL playground.
3. Enter your queries and click the run button to see results instantly.

---

**Note:**
- The SQL playground uses an in-memory SQLite database with a sample `users` table.
- The NoSQL playground uses a sample collection and supports equality, `$gt`, and `$lt` queries.
- All data resets on each run. 