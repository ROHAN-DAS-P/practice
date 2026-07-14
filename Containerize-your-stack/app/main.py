import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import redis
from app.models import Item, ItemCreate
from app.repository import PostgresItemRepository, InMemoryItemRepository
from app.service import ItemService

load_dotenv()

app = FastAPI(title="Layered Architecture Proof")

DATABASE_URL = os.getenv("DATABASE_URL", "")
REDIS_URL = os.getenv("REDIS_URL", "")

# =====================================================================
# THE ARCHITECTURAL PAYOFF
# To revert to in-memory, swap this single line:
# repo = InMemoryItemRepository()
repo = PostgresItemRepository(connection_string=DATABASE_URL)
# =====================================================================

service = ItemService(repository=repo)

@app.get("/health")
def health_check():
    status = {"app": "ok", "database": "unknown", "redis": "unknown"}
    
    # Ping Postgres
    try:
        repo.get_all()
        status["database"] = "connected"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        
    # Ping Redis (Stretch Goal)
    if REDIS_URL:
        try:
            r = redis.from_url(REDIS_URL)
            r.ping()
            status["redis"] = "connected"
        except Exception as e:
            status["redis"] = f"error: {str(e)}"
            
    return status

@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    return service.create_item(item)

@app.get("/items", response_model=list[Item])
def get_items():
    return service.list_items()