FastAPI To-Do List API 📝This is a lightweight, fully functional REST API that manages a to-do list. It was built using Python and FastAPI. It supports the full CRUD cycle (Create, Read, Update, Delete) and validates client input.Currently, the data lives in an in-memory Python list, meaning data resets when the server restarts (a perfect sandbox for learning the Request/Response loop!).🚀 How to Install & RunTo run this API on your local machine, you just need Python installed.Install the required dependencies:pip install fastapi uvicorn
Start the server:uvicorn main:app --reload --port 8000
Open your browser and go to http://localhost:8000/docs to see the interactive Swagger UI!🛣️ EndpointsHTTP MethodEndpointDescriptionStatus CodesGET/API Root / Metadata200 OKGET/healthServer health check200 OKGET/tasksList all tasks200 OKGET/tasks/{id}Get a single task by ID200 OK, 404 Not FoundPOST/tasksCreate a new task201 Created, 400 Bad RequestPUT/tasks/{id}Update an existing task200 OK, 400 Bad Request, 404 Not FoundDELETE/tasks/{id}Remove a task204 No Content, 404 Not Found💻 Sample curl OutputHere is what it looks like to fetch a specific task from the terminal:$ curl -i http://localhost:8000/tasks/1

HTTP/1.1 200 OK
date: Thu, 16 Jul 2026 09:30:00 GMT
server: uvicorn
content-length: 46
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
📸 Interactive Documentation & GalleryFastAPI automatically generates a Swagger UI page based on the code. Below is the main interactive documentation, followed by a comprehensive gallery of the API's functionality across all CRUD stages.Main Swagger UI Dashboard📂 Full API Functionality GalleryNote to viewer: The following screenshots demonstrate the server successfully handling various HTTP methods, status codes, and input validation.Stage / FeatureScreenshotStage 1: Root & Health Check (GET)Stage 2: Read All Tasks (GET)Stage 3: Create Task (POST 201)Stage 3: Validation Error (POST 400)Stage 4: Update Task (PUT 200)Stage 4: Delete Task (DELETE 204)Error Handling: Unknown ID (404 Not Found)Terminal / Curl LogsAdditional View 1Additional View 2