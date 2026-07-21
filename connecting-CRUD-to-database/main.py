from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing a to-do list.",
    version="1.0"
)

# --- IN-MEMORY DATABASE ---
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Master FastAPI", "done": True},
    {"id": 3, "title": "Commit code to GitHub", "done": False}
]

# --- ROOT AND HEALTH ---
@app.get("/", summary="API Root")
def read_root():
    """Returns basic API metadata and available endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health Check")
def health_check():
    """Used by automated systems to verify the server is alive."""
    return {"status": "ok"}

# --- READ ENDPOINTS ---
@app.get("/tasks", summary="List all tasks")
def get_tasks():
    """Returns the complete list of tasks in the database."""
    return tasks

@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id: int):
    """Fetches a specific task by its ID. Returns 404 if missing."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )

# --- CREATE ENDPOINT ---
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(payload: dict):
    """
    Creates a new task. 
    - **title**: Required. Cannot be empty.
    - **done**: Defaults to False.
    """
    title = payload.get("title")
    
    if not title or not str(title).strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )
    
    next_id = max([task["id"] for task in tasks], default=0) + 1
    new_task = {"id": next_id, "title": str(title).strip(), "done": False}
    tasks.append(new_task)
    
    return JSONResponse(status_code=201, content=new_task)

# --- UPDATE AND DELETE ENDPOINTS ---
@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, payload: dict):
    """
    Updates an existing task.
    You can send a new `title`, a new `done` status, or both.
    """
    target_task = None
    for task in tasks:
        if task["id"] == task_id:
            target_task = task
            break
            
    if not target_task:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        
    if not payload:
        return JSONResponse(status_code=400, content={"error": "Request body cannot be empty"})
        
    if "title" in payload:
        title = payload["title"]
        if not title or not str(title).strip():
            return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
        target_task["title"] = str(title).strip()
        
    if "done" in payload:
        target_task["done"] = bool(payload["done"])
        
    return target_task

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    """Removes a task from the database permanently."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)
            
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})