from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing a to-do list.",
    version="1.0"
)

# Stage 0: Hello Server
@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

# Stage 1: Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}