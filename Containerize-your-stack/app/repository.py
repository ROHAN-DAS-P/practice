from abc import ABC, abstractmethod
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from app.models import Item, ItemCreate

class AbstractItemRepository(ABC):
    @abstractmethod
    def create(self, item: ItemCreate) -> Item:
        pass

    @abstractmethod
    def get_all(self) -> List[Item]:
        pass


# 1. THE OLD IN-MEMORY STORE (Kept here to prove the contract)
class InMemoryItemRepository(AbstractItemRepository):
    def __init__(self):
        self._store = {}
        self._id_counter = 1

    def create(self, item: ItemCreate) -> Item:
        new_item = Item(
            id=self._id_counter,
            title=item.title,
            description=item.description,
            created_at="in-memory-timestamp"
        )
        self._store[self._id_counter] = new_item
        self._id_counter += 1
        return new_item

    def get_all(self) -> List[Item]:
        return list(self._store.values())


# 2. THE NEW POSTGRES REPOSITORY
class PostgresItemRepository(AbstractItemRepository):
    def __init__(self, connection_string: str):
        self.conn_str = connection_string

    def _get_connection(self):
        return psycopg2.connect(self.conn_str, cursor_factory=RealDictCursor)

    def create(self, item: ItemCreate) -> Item:
        query = """
            INSERT INTO items (title, description)
            VALUES (%s, %s)
            RETURNING id, title, description, created_at;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (item.title, item.description))
                row = cur.fetchone()
                conn.commit()
                return Item(
                    id=row["id"],
                    title=row["title"],
                    description=row["description"],
                    created_at=str(row["created_at"])
                )

    def get_all(self) -> List[Item]:
        query = "SELECT id, title, description, created_at FROM items ORDER BY id;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    Item(
                        id=row["id"],
                        title=row["title"],
                        description=row["description"],
                        created_at=str(row["created_at"])
                    )
                    for row in rows
                ]