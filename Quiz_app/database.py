import sqlite3

def create_connection():
    conn = sqlite3.connect("quiz.db")
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        name TEXT,
        score INTEGER,
        total INTEGER
    )
    """)

    conn.commit()
    conn.close()

def insert_result(name, score, total):
    conn = create_connection()
    c = conn.cursor()

    c.execute("INSERT INTO results VALUES (?, ?, ?)",
              (name, score, total))

    conn.commit()
    conn.close()