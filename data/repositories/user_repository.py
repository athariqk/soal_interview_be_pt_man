import datetime
from typing import Optional, List, override
from data.adapters.sqlite_repository import SQLiteRepository
from data.models.user import User


class UserRepository(SQLiteRepository):
    def __init__(self, db_path: str = "database.db") -> None:
        super().__init__(db_path, "user", User)

    @override
    def get(self, id: int) -> Optional[User]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return User(
                    name=row["name"],
                    start_date=datetime.date.fromisoformat(row["start_date"]),
                    id=row["id"],
                )
            return None

    @override
    def get_all(self) -> List[User]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            rows = cursor.fetchall()
            return [
                User(
                    name=row["name"],
                    start_date=datetime.date.fromisoformat(row["start_date"]),
                    id=row["id"],
                )
                for row in rows
            ]
