import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.path.join(DATA_DIR, "rooms.db")


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL UNIQUE,
            room_number INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@contextmanager
def get_db():
    conn = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()