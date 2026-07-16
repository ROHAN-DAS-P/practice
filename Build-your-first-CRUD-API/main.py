from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing a to-do list.",
    version="1.0"
)

# --- STAGE 2: IN-MEMORY DATABASE ---
# Pre-filled with 3 example tasks
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Master FastAPI", "done": True},
    {"id": 3, "title": "Commit code to GitHub", "done": False}
]

# --- STAGE 0 & 1: ROOT AND HEALTH ---
@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- STAGE 2: READ ENDPOINTS ---
@app.get("/tasks")
def get_tasks():
    """Returns the whole list of tasks."""
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """
    Returns one task by ID.
    The {task_id} part is a path parameter that FastAPI automatically converts to an integer.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    # Never return an empty 200 for something that doesn't exist
    # Return 404 with custom JSON error message
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

# --- STAGE 3: CREATE ENDPOINT ---
@app.post("/tasks", status_code=201)
def create_task(payload: dict):
    """
    Creates a new task.
    Validates that 'title' exists and is not empty.
    """
    title = payload.get("title")
    
    # Business Rule: Reject missing or empty titles with a 400 Bad Request
    if not title or not str(title).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )
    
    # Calculate the next free ID dynamically
    next_id = max([task["id"] for task in tasks], default=0) + 1
    
    new_task = {
        "id": next_id,
        "title": str(title).strip(),
        "done": False
    }
    
    # Save to our in-memory list
    tasks.append(new_task)
    
    # Return 201 Created with the new task data
    return JSONResponse(status_code=201, content=new_task)
