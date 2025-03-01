import sqlite3
from typing import List
import datetime
from src.model import Task


conn = sqlite3.connect("tasks.db")
c = conn.cursor()


def create_table():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
        description text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
        )
    """
    )


create_table()
