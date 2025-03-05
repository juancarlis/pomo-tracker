import sqlite3
import os

DB_DIR = os.path.expanduser("~/.config/pomo-tracker")
DB_PATH = os.path.join(DB_DIR, "tasks.db")

os.makedirs(DB_DIR, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)
