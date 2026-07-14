# Layered Architecture & Docker Persistence Proof

A production-ready Python FastAPI microservice demonstrating containerized orchestration, clean layered architecture, database persistence across lifecycles, and advanced query optimization.

## 📌 Project Overview

This project serves as a real-world proof of clean architecture and containerization principles:
1. **The Architectural Payoff:** Swapping an in-memory dictionary for a persistent PostgreSQL repository by changing **only one line of configuration**—leaving the service layer, business logic, and API route handlers 100% untouched.
2. **Container Persistence:** Using Docker Compose and named volumes (`pgdata`) to guarantee data survives total container destruction and rebuilding.
3. **Multi-Service Orchestration:** Running an API, PostgreSQL, and Redis cache together in a single bridge network with proper health checks and startup ordering.
4. **Database Optimization:** Demonstrating the quantitative impact of B-Tree indexing on 100,000+ rows using PostgreSQL's `EXPLAIN ANALYZE`.

---

## 🏗️ Architecture & Storage Swap

The application is structured into strict layers:
* **Models (`app/models.py`):** Pydantic data schemas defining input/output contracts.
* **Repository Layer (`app/repository.py`):** Defines `AbstractItemRepository` with two implementations:
  * `InMemoryItemRepository`: Volatile dictionary-based storage.
  * `PostgresItemRepository`: Persistent SQL database storage using `psycopg2`.
* **Service Layer (`app/service.py`):** Contains business logic. **It has zero knowledge of SQL, connections, or dictionaries**; it interacts solely with the abstract repository contract.
* **Composition Root (`app/main.py`):** Reads environment variables and injects the active repository into the service.

### How to Swap Storage
To revert from PostgreSQL back to the in-memory store, change a single line in `app/main.py`:

```python
# From:
repo = PostgresItemRepository(connection_string=DATABASE_URL)

# To:
repo = InMemoryItemRepository()
```
*No other files, routes, or tests need to change.*

---

## 📁 Project Structure

```text
my-project/
├── .env                 # Git-ignored local secrets
├── .env.example         # Committed environment template
├── .gitignore           # Standard Python/Docker ignore rules
├── docker-compose.yml   # Multi-container orchestration
├── Dockerfile           # Python 3.11 slim image build rules
├── init.sql             # Automatic database initialization script
├── requirements.txt     # Python dependencies
└── app/
    ├── __init__.py
    ├── main.py          # FastAPI app, route handlers & composition root
    ├── models.py        # Pydantic schemas
    ├── repository.py    # Abstract contract + In-Memory & Postgres repos
    └── service.py       # Layered business logic
```

---

## 🚀 Getting Started

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* Git installed.

### 2. Environment Setup
Clone the repository and prepare your environment configuration:
```bash
git clone <your-repo-url>
cd my-project
cp .env.example .env
```
*(Note: `.env` is git-ignored to prevent leaking local credentials).*

### 3. Launch the Stack
Start the API, PostgreSQL database, and Redis cache together:
```bash
docker compose up --build -d
```
Verify all containers are up and healthy:
```bash
docker compose ps
```

---

## 🔬 Proving Data Persistence Across Restarts

To verify that the database volume (`pgdata`) holds state across a complete lifecycle shutdown, follow this test protocol:

### Step 1: Verify Stack Connectivity
Check the health endpoint:
```bash
curl http://localhost:8000/health
```
**Expected Response:**
```json
{"app":"ok","database":"connected","redis":"connected"}
```

### Step 2: Create Test Records
Insert two items via the REST API:
```bash
curl -X POST http://localhost:8000/items   -H "Content-Type: application/json"   -d '{"title": "Survive restart", "description": "Proving Docker volume persistence"}'

curl -X POST http://localhost:8000/items   -H "Content-Type: application/json"   -d '{"title": "Layered architecture", "description": "Swapped dict for real repository"}'
```

### Step 3: Verify Creation
Fetch the items to confirm they were assigned PostgreSQL IDs and timestamps:
```bash
curl http://localhost:8000/items
```

### Step 4: Execute the Acid Test (Destroy & Rebuild)
Completely stop and remove all running containers and networks:
```bash
docker compose down
```
*(At this point, `http://localhost:8000` is completely unreachable).*

Bring the stack back up from scratch:
```bash
docker compose up -d
```

### Step 5: Verify Data Recovery
Once containers show `Healthy`/`Started`, fetch the items again:
```bash
curl http://localhost:8000/items
```
**The Payoff:** Both records and their original database timestamps are returned intact. The `pgdata` volume successfully restored the storage state into the newly spun-up database container.

---

## ⚡ Stretch Goal: Database Indexing & Performance Analysis

To prove the impact of B-Tree indexing on database query performance, the `items` table was seeded with 100,000 dummy rows using PostgreSQL's `generate_series()`. We then compared query execution plans using `EXPLAIN ANALYZE` inside the database container.

### 1. Before Indexing (Sequential Scan)
Without an index, PostgreSQL must perform a full sequential disk scan from top to bottom, inspecting and discarding 100,001 rows to find a single match:
```sql
EXPLAIN ANALYZE SELECT * FROM items WHERE title = 'Item 85432';
```
* **Query Plan:** `Seq Scan on items`
* **Rows Removed by Filter:** `100001`
* **Execution Time:** **`6.743 ms`**

### 2. Applying the B-Tree Index
An index was created on the lookup column:
```sql
CREATE INDEX idx_items_title ON items(title);
```

### 3. After Indexing (Bitmap Index Scan)
After indexing, PostgreSQL switched to a B-Tree lookup, eliminating wasted disk reads entirely:
```sql
EXPLAIN ANALYZE SELECT * FROM items WHERE title = 'Item 85432';
```
* **Query Plan:** `Bitmap Index Scan on idx_items_title` -> `Bitmap Heap Scan on items`
* **Heap Blocks Read:** `exact=1` (0 rows discarded)
* **Execution Time:** **`0.074 ms`**

### 📊 Performance Summary
| Metric | Before Index (Seq Scan) | After Index (Bitmap Scan) | Improvement |
| :--- | :--- | :--- | :--- |
| **Scan Method** | Sequential Disk Read | B-Tree / Bitmap Scan | Direct RAM/Page lookup |
| **Wasted Work** | 100,001 rows discarded | 0 rows discarded | 100% precision |
| **Execution Time** | **6.743 ms** | **0.074 ms** | **~91x Faster** |

---

## 🛠️ Helpful Commands

* **View live logs:** `docker compose logs -f`
* **Access interactive Postgres prompt:** `docker compose exec db psql -U postgres -d app_db`
* **Check reserved Windows ports:** `netsh interface ipv4 show excludedportrange protocol=tcp`
* **Stop containers cleanly:** `docker compose down`
* **Wipe volume data completely (reset DB):** `docker compose down -v`