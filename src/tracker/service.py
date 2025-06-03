from datetime import datetime, date, timedelta
from typing import List, Optional

from database import get_connection
from database.database import execute, fetch_all
from tasks.service import get_task_id_from_position
from tracker.models import ActiveTimer, DailySummary
from tracker.queries import STOP_TIME_TRACKING, DAILY_SUMMARY, INSERT_TIME_TRACKING

conn = get_connection()
c = conn.cursor()


def insert_time_tracking(position: int):
    start_time = datetime.now().isoformat()
    task_id = get_task_id_from_position(position)

    execute(INSERT_TIME_TRACKING, (task_id, start_time))


def stop_time_tracking(position: int):
    end_time = datetime.now().isoformat()
    task_id = get_task_id_from_position(position)

    execute(STOP_TIME_TRACKING, (end_time, task_id))


def get_active_timer():
    """
    Retrieve the currently active timer information for tasks.

    This function queries the `time_tracking` table to find all active timers
    that have a non-null `start_time` and a null `end_time`. It joins the
    `tasks` and `categories` tables to provide additional context, including
    the task description and category name.

    Returns:
        list: A list of tuples, each containing:
            - position (int): The position of the task on the list of tasks.
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
          t.position as position,
          t.title as task,
          c.name as category,
          tt.start_time,
          datetime('now', 'localtime') as current_time,
          printf('%02d:%02d:%02d',
          (CAST((julianday(datetime('now', 'localtime')) - julianday(tt.start_time)) * 86400 AS INTEGER) / 3600) % 24,
          (CAST((julianday(datetime('now', 'localtime')) - julianday(tt.start_time)) * 86400 AS INTEGER) / 60) % 60,
          (CAST((julianday(datetime('now', 'localtime')) - julianday(tt.start_time)) * 86400 AS INTEGER) % 60)
            ) as elapsed_time
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
            position=result[0],
            task=result[1],
            category=result[2],
            start_time=datetime.fromisoformat(result[3]),
            current_time=datetime.fromisoformat(result[4]),
            elapsed_time=result[5],
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


def get_daily_summary(
    date_str: Optional[str] = "", relative_days: int = 0
) -> List[DailySummary]:
    """
    Fetch tracking summary for a specific day.
    Either `date_str` (format YYYY-MM-DD) or `relative_days` must be used.
    If both are default, defaults to today.
    """

    if date_str and relative_days != 0:
        raise ValueError("Only one of date_str or relative_days should be provided.")

    if date_str:
        try:
            query_date = date.fromisoformat(date_str)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    else:
        query_date = date.today() + timedelta(days=relative_days)

    str_date = query_date.strftime("%Y-%m-%d")
    return fetch_all(
        DAILY_SUMMARY, lambda row: DailySummary(*row), params=(str_date, str_date)
    )
