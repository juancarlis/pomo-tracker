import sqlite3
from datetime import datetime

from src.tracker.models import ActiveTimer


conn = sqlite3.connect("tasks.db")
c = conn.cursor()


def insert_time_tracking(task_id: int):
    start_time = datetime.now().isoformat()

    with conn:
        c.execute(
            """
            INSERT INTO time_tracking (task_id, start_time)
            VALUES(?, ?)
            """,
            (task_id, start_time),
        )


def stop_time_tracking(task_id: int):
    end_time = datetime.now().isoformat()

    with conn:
        c.execute(
            """
            UPDATE time_tracking
            SET end_time = ?
            WHERE task_id = ? AND end_time IS NULL
            """,
            (end_time, task_id),
        )


def get_active_timer():
    """
    Retrieve the currently active timer information for tasks.

    This function queries the `time_tracking` table to find all active timers
    that have a non-null `start_time` and a null `end_time`. It joins the
    `tasks` and `categories` tables to provide additional context, including
    the task description and category name.

    Returns:
        list: A list of tuples, each containing:
            - task (str): The description of the task.
            - category (str): The name of the category associated with the task.
            - start_time (str): The start time of the timer in ISO format.
            - current_time (str): The current time in ISO format.
            - elapsed_time_seconds (float): The elapsed time in seconds since the timer started.
            - elapsed_time_minutes (float): The elapsed time in minutes since the timer started.
    """

    c.execute(
        """
        SELECT
          t.description as task,
          c.name as category,
          tt.start_time,
          datetime('now', 'localtime') as current_time,
          (julianday('now', 'localtime') - julianday(tt.start_time)) * 86400 as elapsed_time_seconds,
          (julianday('now', 'localtime') - julianday(tt.start_time)) * 1440 as elapsed_time_minutes
        FROM time_tracking tt
        LEFT JOIN tasks t ON t.id = tt.task_id
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE 1=1
          AND end_time IS NULL
          AND start_time IS NOT NULL;
        """
    )
    result = c.fetchone()

    if result:
        return ActiveTimer(
            task=result[0],
            category=result[1],
            start_time=datetime.fromisoformat(result[2]),
            current_time=datetime.fromisoformat(result[3]),
            elapsed_time_seconds=result[4],
            elapsed_time_minutes=result[5],
        )

    return None


def get_task_total_time(task_id: int):
    c.execute(
        """
        SELECT
            SUM(julianday(end_time) - julianday(start_time)) * 86400
        FROM time_tracking
        WHERE task_id = ? AND end_time IS NOT NULL
        """,
        (task_id,),
    )

    result = c.fetchone()
    return result[0] if result[0] else 0
