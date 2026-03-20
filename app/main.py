from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Todo API is running"}

def get_db_connection():
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.get("/api/todos")
def get_todos():
    conn = get_db_connection()
    todos = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()

    return [dict(todo) for todo in todos]