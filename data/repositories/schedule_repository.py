from typing import Optional, List, override
from data.adapters.sqlite_repository import SQLiteRepository
from data.models.schedule import Schedule, Shift
from data.models.user import User


class ScheduleRepository(SQLiteRepository):
    def __init__(self, db_path: str = "database.db") -> None:
        super().__init__(db_path, "schedule", Schedule)
    
    @override
    def get(self, id: int) -> Optional[Schedule]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schedule WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return Schedule(
                    user_id=row["user_id"],
                    shift=Shift(row["shift"]),
                    day=row["day"],
                    id=row["id"]
                )
            return None
    
    @override
    def get_all(self) -> List[Schedule]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schedule")
            rows = cursor.fetchall()
            return [
                Schedule(
                    user_id=row["user_id"],
                    shift=Shift(row["shift"]),
                    day=row["day"],
                    id=row["id"]
                )
                for row in rows
            ]
    
    def get_by_user(self, user_id: int) -> List[Schedule]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schedule WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            return [
                Schedule(
                    user_id=row["user_id"],
                    shift=Shift(row["shift"]),
                    day=row["day"],
                    id=row["id"]
                )
                for row in rows
            ]
