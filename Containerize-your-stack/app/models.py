from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Item(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_at: Optional[str] = None