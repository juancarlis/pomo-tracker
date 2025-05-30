from contextlib import contextmanager
import os
import sqlite3
from typing import Any, Callable, Optional

DB_DIR = os.path.expanduser("~/.config/pomo-tracker")
DB_PATH = os.path.join(DB_DIR, "tasks.db")

os.makedirs(DB_DIR, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


@contextmanager
def db_cursor():
    conn = get_connection()
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()


def fetch_all(query: str, mapper: Callable, params: tuple = ()) -> list:
    with db_cursor() as cursor:
        cursor.execute(query, params)
        return [mapper(row) for row in cursor.fetchall()]


def fetch_one(query: str, mapper: Callable, params: tuple = ()) -> Optional[Any]:
    with db_cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchone()
        return mapper(result) if result else None


def execute(query: str, params: tuple = ()) -> Any:
    with db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.lastrowid
