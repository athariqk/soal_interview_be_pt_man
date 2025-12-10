import sqlite3
from pathlib import Path

from data.models.schedule import Shift


def create_tables(cursor: sqlite3.Cursor):
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL
        )
    """)
    
    # Schedules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            shift INTEGER NOT NULL,
            day INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    """)


def seed_tables(cursor: sqlite3.Cursor):
    cursor.execute("SELECT COUNT(*) FROM user")
    if cursor.fetchone()[0] == 0:
        initial_users = [
            ("Ahmad", "2024-12-26",),
            ("Widi", "2024-12-26",),
            ("Yono", "2024-12-26",),
            ("Yohan", "2024-12-26",)
        ]
        cursor.executemany("INSERT INTO user (name, start_date) VALUES (?, ?)", initial_users)
        print("Seeded initial users data")
        
    cursor.execute("SELECT COUNT(*) FROM schedule")
    if cursor.fetchone()[0] == 0:
        initial_shifts = [
            (1, Shift.P.value, 0),
            (1, Shift.P.value, 1),
            (1, Shift.S.value, 2),
            (1, Shift.S.value, 3),
            (1, Shift.M.value, 4),
            (1, Shift.M.value, 5),
            (1, Shift.L.value, 6),
            (2, Shift.S.value, 0),
            (2, Shift.S.value, 1),
            (2, Shift.M.value, 2),
            (2, Shift.M.value, 3),
            (2, Shift.L.value, 4),
            (2, Shift.P.value, 5),
            (2, Shift.S.value, 6),
            (3, Shift.M.value, 0),
            (3, Shift.M.value, 1),
            (3, Shift.P.value, 2),
            (3, Shift.L.value, 3),
            (3, Shift.P.value, 4),
            (3, Shift.P.value, 5),
            (3, Shift.M.value, 6),
            (4, Shift.L.value, 0),
            (4, Shift.P.value, 1),
            (4, Shift.P.value, 2),
            (4, Shift.P.value, 3),
            (4, Shift.S.value, 4),
            (4, Shift.S.value, 5),
            (4, Shift.P.value, 6),
            (4, Shift.L.value, 7),
            (4, Shift.S.value, 8),
            (4, Shift.S.value, 9),
            (4, Shift.P.value, 10),
            (4, Shift.S.value, 11),
            (4, Shift.S.value, 12),
            (4, Shift.P.value, 13),
        ]
        cursor.executemany("INSERT INTO schedule (user_id, shift, day) VALUES (?, ?, ?)", initial_shifts)
        print("Seeded initial shifts data")


def init_database(db_path: str = "database.db") -> None:
    Path(db_path).touch(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    create_tables(cursor)
    seed_tables(cursor)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")


if __name__ == "__main__":
    init_database()
