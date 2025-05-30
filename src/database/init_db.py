import logging

from database import DB_PATH, get_connection
from database.database import execute
from database.queries import (
    DDL_CREATE_CATEGORIES_TABLE,
    DDL_CREATE_TASKS_CONTENT_TABLE,
    DDL_CREATE_TASKS_TABLE,
    INSERT_DEFAULT_CATEGORIES,
)


conn = get_connection()
c = conn.cursor()

TABLE_TASKS = "tasks"
TABLE_CATEGORIES = "categories"
TABLE_TRACKER = "time_tracking"
TABLE_ALARMS = "alarms"
TABLE_CONTENTS = "table_contents"


def create_tasks_table():
    execute(DDL_CREATE_TASKS_TABLE)
    logging.info(f"Tasks table created at {DB_PATH}")


def create_categories_table():
    execute(DDL_CREATE_CATEGORIES_TABLE)
    logging.info(f"Tasks categories created at {DB_PATH}")


def insert_default_categories():
    execute(INSERT_DEFAULT_CATEGORIES)
    logging.info("Tasks categories populated")


def create_time_tracking_table():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS time_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            start_time TEXT NOT NULL,
            end_time TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        );
        """
    )
    logging.info(f"Time tracking table created at {DB_PATH}")


def create_alarms_table():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS alarms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            status TEXT CHECK(status IN ('pending', 'finished', 'stopped')) DEFAULT 'pending',
            recurring INTEGER NOT NULL DEFAULT 0 -- 0 = no recurrente, 1 = recurrente
        );
        """
    )
    logging.info(f"Alarms table created at {DB_PATH}")


def create_tasks_contents_table():
    execute(DDL_CREATE_TASKS_CONTENT_TABLE)
    logging.info("Tasks contents table created")


def create_context_table():
    c.execute(
        """

    """
    )


def create_database():

    create_tasks_table()
    create_categories_table()
    create_tasks_contents_table()
    insert_default_categories()
    create_time_tracking_table()
    create_alarms_table()

    conn.commit()
    conn.close()
