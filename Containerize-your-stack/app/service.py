from typing import List
from app.repository import AbstractItemRepository
from app.models import Item, ItemCreate

class ItemService:
    def __init__(self, repository: AbstractItemRepository):
        self.repository = repository

    def create_item(self, item_data: ItemCreate) -> Item:
        # Business logic, validation, or logging goes here
        return self.repository.create(item_data)

    def list_items(self) -> List[Item]:
        return self.repository.get_all()