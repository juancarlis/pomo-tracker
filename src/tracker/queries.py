INSERT_TIME_TRACKING = """
    INSERT INTO time_tracking (task_id, start_time)
    VALUES(?, ?)
"""


STOP_TIME_TRACKING = """
    UPDATE time_tracking
    SET end_time = ?
    WHERE task_id = ? AND end_time IS NULL
"""


DAILY_SUMMARY = """
    WITH tracker_data AS (
      SELECT
        tt.id,
        tt.start_time,
        tt.end_time,
        (strftime('%s', end_time) - strftime('%s', start_time)) as seconds_elapsed,
        t.title as task,
        c.name as category,
        t.deleted,
        t."status"
      FROM time_tracking tt
      JOIN tasks t ON t.id = tt.task_id
      JOIN categories c ON c.id = t.category_id
    )
    SELECT
      id,
      task,
      category,
      -- seconds_elapsed,
      ROUND((seconds_elapsed / 60.0), 2) AS minutes_elapsed,
      ROUND((seconds_elapsed / 3600.0), 2) AS hours_elapsed,
      strftime('%Y-%m-%d %H:%M', start_time) as start_time,
      strftime('%Y-%m-%d %H:%M', end_time) as end_time
    FROM tracker_data
    WHERE 1 = 1
      AND (
          strftime('%Y-%m-%d', start_time) = ?
          OR  strftime('%Y-%m-%d', end_time) = ?
          )
"""
