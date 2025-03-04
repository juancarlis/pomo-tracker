import sqlite3
from typing import List, Optional
import datetime
from src.tasks.models import PendingTaskDTO, Task
from src.categories.service import get_category_id_from_name

conn = sqlite3.connect("tasks.db")
c = conn.cursor()


def get_all_tasks() -> List[Task]:
    c.execute(
        """
    SELECT
      t.id,
      t.title,
      c.name as category,
      t.date_added,
      t.date_completed,
      t.status,
      t.position
    FROM tasks t
    LEFT JOIN categories c ON c.id = t.category_id
    WHERE t.deleted = 0
    ;
    """
    )
    results = c.fetchall()
    tasks = []
    for result in results:
        tasks.append(Task(*result))
    return tasks


def get_pending_tasks() -> List[PendingTaskDTO]:
    c.execute(
        """
        SELECT
          t.position,
          t.title,
          c.name as category_name,
          t.date_added,
          CASE
            WHEN start_time IS NOT NULL AND end_time IS NULL
              THEN 1
            ELSE NULL
          END AS tracking
        FROM tasks t
        LEFT JOIN categories c ON c.id = t.category_id
        LEFT JOIN time_tracking tt ON tt.task_id = t.id
        WHERE 1=1
          AND deleted = 0
          AND t.status = 0
        ;
    """
    )
    results = c.fetchall()
    return [PendingTaskDTO(*result) for result in results]


def insert_task(task: Task):
    c.execute("SELECT COUNT(1) FROM tasks")
    count = c.fetchone()[0]
    task.position = count + 1 if count else 1

    with conn:
        c.execute(
            """
            INSERT INTO tasks (title, category_id, date_added, date_completed, status, position)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                task.title,
                task.category_id,
                task.date_added,
                task.date_completed,
                task.status,
                task.position,
            ),
        )

        task.id = c.lastrowid


def delete_task(position: int):
    """Soft deletes a task by updating deleted to True in db."""
    c.execute("SELECT COUNT(*) FROM tasks")
    count = c.fetchone()[0]

    with conn:
        c.execute(
            """
        UPDATE tasks
            SET deleted = 1
        WHERE position=:position
        """,
            {"position": position},
        )
        for pos in range(position + 1, count + 1):
            change_position(pos, pos - 1, False)


def change_position(old_position: int, new_position: int, commit=True):
    c.execute(
        "UPDATE tasks SET position = :position_new WHERE position = :position_old",
        {"position_old": old_position, "position_new": new_position},
    )
    if commit:
        conn.commit()


def update_task(position: int, title: str, category: str):
    with conn:
        if title is not None and category is not None:
            c.execute(
                "UPDATE tasks SET title = :title, category = :category WHERE position = :position",
                {
                    "position": position,
                    "title": title,
                    "category": category,
                },
            )
        if title is not None:
            c.execute(
                "UPDATE tasks SET title = :title WHERE position = :position",
                {"position": position, "title": title},
            )
        if category is not None:
            c.execute(
                "UPDATE tasks SET category = :category WHERE position = :position",
                {"position": position, "category": category},
            )


def complete_task(position: int):
    c.execute("SELECT COUNT(*) FROM tasks")
    count = c.fetchone()[0]
    with conn:
        c.execute(
            """
            UPDATE tasks
            SET status = 1,
                date_completed = :date_completed,
                position = 0
            WHERE position = :position
            """,
            {
                "position": position,
                "date_completed": datetime.datetime.now().isoformat(),
            },
        )

        for pos in range(position + 1, count + 1):
            change_position(pos, pos - 1, False)


def get_task_id_from_position(position: int) -> Optional[int]:
    with conn:
        c.execute(
            """
            SELECT id FROM tasks WHERE position = :position
            """,
            {"position": position},
        )
        result = c.fetchone()
        if result:
            return result[0]
        return None
