import sqlite3
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing a to-do list with SQLite persistence.",
    version="2.0"
)

DATABASE_NAME = "tasks.db"

# --- HELPER FUNCTION: DATABASE CONNECTION ---
def get_db_connection():
    """Creates a connection to the SQLite database and allows dictionary-like row access."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- STAGE 0: DATABASE INITIALIZATION & SEEDING ---
@app.on_event("startup")
def init_db():
    """
    Creates the tasks table if it doesn't exist.
    If the table is completely empty, seeds it with 3 example tasks.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    
    # Check if table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    # Seed initial data only if empty
    if count == 0:
        example_tasks = [
            ("Buy milk", False),
            ("Master FastAPI", True),
            ("Commit code to GitHub", False)
        ]
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", example_tasks)
        print("Database initialized and seeded with 3 example tasks!")
    else:
        print("Database already contains data. Skipping seed step.")
        
    conn.commit()
    conn.close()

# --- ROOT AND HEALTH ---
@app.get("/", summary="API Root")
def read_root():
    """Returns basic API metadata and available endpoints."""
    return {"name": "Task API", "version": "2.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health Check")
def health_check():
    """Used by automated systems to verify the server is alive."""
    return {"status": "ok", "database": "connected"}

# --- STAGE 1: READ ENDPOINTS ---
@app.get("/tasks", summary="List all tasks")
def get_tasks():
    """Returns the complete list of tasks directly from the SQLite database."""
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    
    # Convert sqlite3.Row objects to standard dictionaries and booleans
    return [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in tasks]

@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    """Fetches a specific task by ID from SQLite. Returns 404 if missing."""
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
        
    return {"id": task["id"], "title": task["title"], "done": bool(task["done"])}

# --- STAGE 2: CREATE ENDPOINT ---
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(payload: dict):
    """
    Inserts a new task row into the SQLite database.
    - **title**: Required. Cannot be empty.
    - **done**: Defaults to False.
    """
    title = payload.get("title")
    
    # Validation Rule: Reject missing or empty titles
    if not title or not str(title).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )
        
    clean_title = str(title).strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    # Notice we use parameterized queries (?) to prevent SQL injection!
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (clean_title, False))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"id": new_id, "title": clean_title, "done": False}

# --- STAGE 3: UPDATE AND DELETE ENDPOINTS ---
@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, payload: dict):
    """Updates an existing task row in the SQLite database."""
    if not payload:
        return JSONResponse(status_code=400, content={"error": "Request body cannot be empty"})
        
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    
    if task is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        
    # Determine new values based on existing data or payload updates
    new_title = task["title"]
    if "title" in payload:
        title_val = payload["title"]
        if not title_val or not str(title_val).strip():
            conn.close()
            return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
        new_title = str(title_val).strip()
        
    new_done = bool(task["done"])
    if "done" in payload:
        new_done = bool(payload["done"])
        
    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, task_id)
    )
    conn.commit()
    conn.close()
    
    return {"id": task_id, "title": new_title, "done": new_done}

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Removes a task row from the SQLite database permanently."""
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    
    if task is None:
        conn.close()
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return Response(status_code=204)