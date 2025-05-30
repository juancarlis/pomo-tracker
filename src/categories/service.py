from typing import List, Optional

from categories.models import Category
from categories.queries import (
    SELECT_CATEGORY_ID_FROM_ID,
    SELECT_CATEGORY_ID_FROM_NAME,
)
from database import fetch_one, get_connection


conn = get_connection()
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


def get_category_id_from_name_or_id(category: str) -> Optional[int]:
    """
    Gets the category id from a category name or an id in string format.
    """

    try:
        category_id = int(category)
        return fetch_one(
            query=SELECT_CATEGORY_ID_FROM_ID,
            mapper=lambda row: row[0],
            params=(category_id,),
        )
    except ValueError:
        return fetch_one(
            query=SELECT_CATEGORY_ID_FROM_NAME,
            mapper=lambda row: row[0],
            params=(category,),
        )
