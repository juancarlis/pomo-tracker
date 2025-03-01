import sqlite3
from typing import List
import datetime
from src.tasks.models import Task

conn = sqlite3.connect("tasks.db")
c = conn.cursor()


def get_all_tasks() -> List[Task]:
    c.execute("SELECT * FROM tasks")
    results = c.fetchall()
    tasks = []
    for result in results:
        tasks.append(Task(*result))
    return tasks


def insert_task(task: Task):
    c.execute("SELECT COUNT(1) FROM tasks")
    count = c.fetchone()[0]
    task.position = count if count else 0
    with conn:
        c.execute(
            "INSERT INTO tasks VALUES (:description, :category, :date_added, :date_completed, :status, :position)",
            {
                "description": task.description,
                "category": task.category,
                "date_added": task.category,
                "date_completed": task.date_completed,
                "status": task.status,
                "position": task.position,
            },
        )


def delete_task(position: int):
    c.execute("SELECT COUNT(*) FROM tasks")
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE FROM tasks WHERE position=:position", {"position": position})
        for pos in range(position + 1, count):
            change_position(pos, pos - 1, False)


def change_position(old_position: int, new_position: int, commit=True):
    c.execute(
        "UPDATE tasks SET position = :position_new WHERE position = :position_old",
        {"position_old": old_position, "position_new": new_position},
    )
    if commit:
        conn.commit()


def update_task(position: int, description: str, category: str):
    with conn:
        if description is not None and category is not None:
            c.execute(
                "UPDATE tasks SET description = :description, category = :category WHERE position = :position",
                {
                    "position": position,
                    "description": description,
                    "category": category,
                },
            )
        if description is not None:
            c.execute(
                "UPDATE tasks SET description = :description WHERE position = :position",
                {"position": position, "description": description},
            )
        if category is not None:
            c.execute(
                "UPDATE tasks SET category = :category WHERE position = :position",
                {"position": position, "category": category},
            )


def complete_task(position: int):
    with conn:
        c.execute(
            "UPDATE tasks SET status = 1, date_completed = :date_completed WHERE position = :position",
            {
                "position": position,
                "date_completed": datetime.datetime.now().isoformat(),
            },
        )
