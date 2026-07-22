# 📋 Task API – SQLite Persistence Upgrade

A RESTful CRUD API built with **Python**, **FastAPI**, and **SQLite** for managing a to-do list.

This project upgrades the original in-memory task storage to a persistent **SQLite** database. The API endpoints and behavior remain the same, but all task data is now stored permanently in a database file, allowing data to persist even after the server is restarted.

---

# 🚀 Features

- ✅ Create, Read, Update, and Delete (CRUD) tasks
- ✅ Persistent data storage using SQLite
- ✅ Automatic database creation on first run
- ✅ Automatic table creation and initial data seeding
- ✅ Interactive Swagger API documentation
- ✅ Input validation and proper HTTP status codes

---

# 🏗️ Project Structure

```
.
├── main.py
├── tasks.db               # Automatically created on first run
├── README.md
└── requirements.txt
```

---

# 🐍 Why SQLite Was Chosen

SQLite was selected as the database for this project because:

- **Serverless Database** – No separate database server installation is required.
- **Lightweight** – The complete database is stored in a single file.
- **Easy Setup** – Python includes built-in support through the `sqlite3` module.
- **Perfect for Small Projects** – Ideal for learning SQL and building REST APIs.
- **Portable** – The entire database can be moved simply by copying one file.

---

# 💾 Database Storage

The application stores all data in a local SQLite database file named:

```
tasks.db
```

The file is automatically created in the **root directory of the project** the first time the application starts.

If the database does not exist, the application will automatically:

- Create `tasks.db`
- Create the `tasks` table
- Insert the default sample tasks

This means anyone cloning the repository can simply run the application and the database will be created automatically.

---

# ⚙️ Requirements

- Python 3.10 or newer
- pip

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

---

## 2. (Optional) Create a Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not available:

```bash
pip install fastapi uvicorn
```

---

## 4. Run the Application

```bash
uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

## 5. Open the Interactive API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# ✅ Automatic Database Creation

On the **first run**, the application automatically:

- Creates `tasks.db`
- Creates the required database table
- Seeds the database with sample tasks

No manual SQL commands or setup are required.

To reset the database, simply delete:

```
tasks.db
```

Then restart the server.

---

# 🗄️ Database Schema

| Column | Type    | Description                             |
| ------ | ------- | --------------------------------------- |
| id     | INTEGER | Primary Key (Auto Increment)            |
| title  | TEXT    | Task title                              |
| done   | BOOLEAN | Completion status (0 = False, 1 = True) |

---

# 📝 Example SQL Query

During testing in **DBeaver Community Edition (CE)**, the following SQL query was executed to display all completed tasks.

```sql
SELECT *
FROM tasks
WHERE done = 1;
```

---

# 🌐 API Endpoints

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/`           | API welcome message     |
| GET    | `/health`     | Health check            |
| GET    | `/tasks`      | Retrieve all tasks      |
| GET    | `/tasks/{id}` | Retrieve a task by ID   |
| POST   | `/tasks`      | Create a new task       |
| PUT    | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task           |

---

# 📸 Screenshots

## 1. DBeaver CE Database Viewer

> Replace the placeholder below with your database viewer screenshot.

```
Insert Screenshot Here

Suggested filename:
dbeaver-database-viewer.png
```

Or use Markdown once the image is added:

```markdown
![DBeaver Database Viewer](/images/dbeaver-database-viewer.png)
```

---

## 2. SQL Query Executed in DBeaver CE

> Replace the placeholder below with the screenshot showing the SQL query execution.

```
Insert Screenshot Here

Suggested filename:
dbeaver-sql-query.png
```

Or use Markdown once the image is added:

```markdown
![SQL Query Executed](/images/dbeaver-sql-query.png)
```

---

# 🧪 Testing the API

Example request using cURL:

```bash
curl http://127.0.0.1:8000/tasks
```

Example POST request:

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
-H "Content-Type: application/json" \
-d "{\"title\":\"Learn SQLite\"}"
```

---

# 🛠️ Helpful Commands

Run the server:

```bash
uvicorn main:app --reload
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Reset the database:

Delete:

```
tasks.db
```

Restart the server:

```bash
uvicorn main:app --reload
```

The application will automatically recreate the database.

---

# ✅ Checkpoint

Anyone cloning this repository can:

1. Clone the project.
2. Install the dependencies.
3. Run the FastAPI server.
4. Have the SQLite database (`tasks.db`) automatically created.
5. Start using the API immediately without any additional database setup.

---

## Built With

- Python
- FastAPI
- SQLite
- sqlite3
- Uvicorn
- DBeaver Community Edition (CE)
