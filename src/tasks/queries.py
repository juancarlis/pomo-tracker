SELECT_ALL_TASKS = """
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


SELECT_PENDING_TASKS = """
    SELECT
      t.position,
      t.title,
      c.name AS category_name,
      t.date_added,
      CASE
        WHEN EXISTS (
          SELECT 1
          FROM time_tracking tt2
          WHERE tt2.task_id = t.id
            AND tt2.end_time IS NULL
        )
        THEN 1
        ELSE 0
      END AS tracking
    FROM tasks t
    LEFT JOIN categories c ON c.id = t.category_id
    WHERE t.deleted = 0
      AND t.status = 0
    ORDER BY t.position;
    """


SELECT_TASK_ID_FROM_POSITION = " SELECT id FROM tasks WHERE position = ? "


COUNT_TASKS = "SELECT COUNT(1) FROM tasks"


COUNT_UNDELETED = "SELECT COUNT(1) FROM tasks WHERE deleted = 0 AND status = 0"


COMPLETE_TASKS = """
        UPDATE tasks
        SET status = 1,
            date_completed = ?,
            position = 0
        WHERE position = ?
        ;
"""

SHIFT_POSITIONS_AFTER_DELETE = """
    UPDATE tasks
        SET position = position - 1
    WHERE deleted = 0
        AND status = 0
        AND position > ?;
"""

INSERT_TASK = """
    INSERT INTO tasks (title, category_id, date_added, date_completed, status, position)
    VALUES (?, ?, ?, ?, ?, ?)
    ;
"""


DELETE_TASK = """
    UPDATE tasks
        SET deleted = 1, position = 0
    WHERE id = ?;
"""


UPDATE_TASK_TITLE = """
    UPDATE tasks SET title = ? WHERE position = ?;
"""

UPDATE_TASK_CATEGORY = """
    UPDATE tasks SET category_id = ? WHERE position = ?;
"""

UPDATE_TASK_TITLE_CATEGORY = """
    UPDATE tasks SET title = ?, category_id = ? WHERE position = ?;
"""


# Tasks contents

INSERT_TASK_CONTENT = """
    INSERT INTO tasks_contents (task_id, content)
    VALUES (?, ?);
"""

SELECT_TASK_CONTENT = """
    SELECT content FROM tasks_contents
    WHERE task_id = ?
    ORDER BY created_at DESC
    LIMIT 1;
"""

UPDATE_TASK_CONTENT = """
    UPDATE tasks_contents
    SET content = ?, created_at = CURRENT_TIMESTAMP
    WHERE task_id = ?;
"""
