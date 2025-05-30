from typing import List, Optional
import datetime

from categories.service import get_category_id_from_name_or_id
from database import execute, fetch_all, fetch_one
from tasks.models import PendingTaskDTO, Task
from tasks.queries import (
    CHANGE_POSITION,
    COMPLETE_TASKS,
    COUNT_UNDELETED,
    DELETE_TASK,
    INSERT_TASK,
    INSERT_TASK_CONTENT,
    SELECT_ALL_TASKS,
    SELECT_PENDING_TASKS,
    SELECT_TASK_CONTENT,
    SELECT_TASK_ID_FROM_POSITION,
    UPDATE_TASK_CATEGORY,
    UPDATE_TASK_CONTENT,
    UPDATE_TASK_TITLE,
    UPDATE_TASK_TITLE_CATEGORY,
)


def get_all_tasks() -> List[Task]:
    return fetch_all(SELECT_ALL_TASKS, lambda row: Task(*row))


def get_pending_tasks() -> List[PendingTaskDTO]:
    return fetch_all(SELECT_PENDING_TASKS, lambda row: PendingTaskDTO(*row))


def insert_task(task: Task):
    count = fetch_all(COUNT_UNDELETED, lambda row: row[0])[0]
    task.position = count + 1 if count else 1

    task.id = execute(
        INSERT_TASK,
        (
            task.title,
            task.category_id,
            task.date_added,
            task.date_completed,
            task.status,
            task.position,
        ),
    )


def delete_task(position: int):
    """Soft deletes a task by updating deleted to True in db."""

    execute(DELETE_TASK, (position,))
    _adjust_positions(position)


def update_task(position: int, title: str, category: Optional[str]) -> None:
    """
    Updates the task at 'position' with the new 'title' and/or 'category'.
    If 'category' is not None, it will be resolved to an ID (if possible).
    """

    category_id = None
    if category is not None:
        category_id = get_category_id_from_name_or_id(category)

    if title is not None and category is not None:
        execute(UPDATE_TASK_TITLE_CATEGORY, (title, category_id, position))

    if title is not None:
        execute(UPDATE_TASK_TITLE, (title, position))

    if category is not None:
        execute(UPDATE_TASK_CATEGORY, (category_id, position))


def get_task_id_from_position(position: int) -> Optional[int]:
    return fetch_one(
        SELECT_TASK_ID_FROM_POSITION, mapper=lambda row: row[0], params=(position,)
    )


def complete_task(position: int):
    execute(COMPLETE_TASKS, (datetime.datetime.now().isoformat(), position))
    _adjust_positions(position)


def _adjust_positions(position):
    count = fetch_all(COUNT_UNDELETED, lambda row: row[0])[0]
    for pos in range(position + 1, count + 1):
        _change_position(pos, pos - 1)


def _change_position(old_position: int, new_position: int):
    execute(CHANGE_POSITION, (new_position, old_position))


def get_task_content(task_id: int) -> Optional[str]:
    return fetch_one(SELECT_TASK_CONTENT, params=(task_id,), mapper=lambda row: row[0])


def insert_task_content(task_id: int, content: str) -> None:
    execute(INSERT_TASK_CONTENT, (task_id, content))


def update_task_content(task_id: int, content: str) -> None:
    execute(UPDATE_TASK_CONTENT, (content, task_id))
