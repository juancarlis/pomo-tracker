import sqlite3
from contextlib import closing

DB_PATH = "tasks.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
