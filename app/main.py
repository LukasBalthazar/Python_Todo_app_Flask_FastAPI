from fastapi import FastAPI, Request, HTTPException
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

@app.post("/api/todos")
async def add_todo(request: Request):
    data = await request.json()

    if not data or "title" not in data:
        return {"error": "Title is required"}
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO todos (title, completed) VALUES (?, ?)",
        (data["title"], data.get("completed", False))
    )

    conn.commit()

    new_todo_id = cursor.lastrowid
    new_todo = conn.execute(
        "SELECT * FROM todos WHERE id = ?",
        (new_todo_id,)
    ).fetchone()

    conn.close()

    return dict(new_todo)

@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int):
    conn = get_db_connection()

    todo = conn.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    ).fetchone()

    conn.close()

    if todo is None:
        return {"error": "Todo not found"}
    
    return dict(todo)

@app.put("/api/todos/{todo_id}")
async def updated_todo(todo_id: int, request: Request):
    data = await request.json()

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    
    conn = get_db_connection()

    existing_todo = conn.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    ).fetchone()

    if existing_todo is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    
    updated_title = data.get("title", existing_todo["title"])
    updated_completed = data.get("completed", existing_todo["completed"])

    conn.execute(
        "UPDATE todos SET title = ?, completed = ? WHERE id = ?",
        (updated_title, updated_completed, todo_id)
    )
    conn.commit()

    updated_todo = conn.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    ).fetchone()

    conn.close()

    return dict(updated_todo)

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db_connection()

    existing_todo = conn.execute(
        "SELECT * FROM todos WHERE id = ?",
        (todo_id,)
    ).fetchone()

    if existing_todo is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    
    conn.execute(
        "DELETE FROM todos WHERE id = ?",
        (todo_id,)
    )
    conn.commit()
    conn.close()

    return {"message": "Todo deleted succesfully"}