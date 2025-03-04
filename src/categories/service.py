import sqlite3
from typing import List, Optional

from src.categories.models import Category


conn = sqlite3.connect("tasks.db")
c = conn.cursor()


def get_all_categories() -> List[Category]:
    c.execute("SELECT * FROM categories")
    results = c.fetchall()
    categories = []
    for result in results:
        categories.append(Category(*result))
    return categories


def get_category_id_from_name(category_name: str) -> Optional[int]:

    try:
        category_id = int(category_name)
        c.execute("SELECT id FROM categories WHERE id = ?", (category_id,))
    except ValueError:
        c.execute("SELECT id FROM categories WHERE name = ?", (category_name,))

    result = c.fetchone()
    return result[0] if result else None
