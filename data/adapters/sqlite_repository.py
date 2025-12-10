import sqlite3
from typing import Optional, Sequence
from contextlib import contextmanager
from data.base_classes.abstract_repository import AbstractRepository
from data.base_classes.model import Model


class SQLiteRepository(AbstractRepository):
    def __init__(self, db_path: str, table_name: str, model_class) -> None:
        self.db_path = db_path
        self.table_name = table_name
        self.model_class = model_class
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def add(self, model: Model) -> Model:
        raise NotImplementedError
    
    def get(self, id: int) -> Optional[Model]:
        raise NotImplementedError
    
    def get_all(self) -> Sequence[Model]:
        raise NotImplementedError
    
    def update(self, model: Model) -> Optional[Model]:
        raise NotImplementedError
    
    def delete(self, id: int) -> bool:
        raise NotImplementedError
