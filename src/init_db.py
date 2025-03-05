import logging
import sqlite3


conn = sqlite3.connect("tasks.db")
c = conn.cursor()

DB_PATH = "tasks.db"


def create_tasks_table():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        category_id INTEGER,
        date_added TEXT,
        date_completed TEXT,
        status INTEGER,
        position INTEGER,
        deleted INTEGER DEFAULT 0, --soft delete (0 = active, 1 = deleted)

        FOREIGN KEY (category_id) REFERENCES categories(id)
        ) STRICT;
    """
    )
    logging.info(f"Tasks table created at {DB_PATH}")


def create_categories_table():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        color TEXT
        );
        """
    )
    logging.info(f"Tasks categories created at {DB_PATH}")


def insert_default_categories():
    c.execute(
        """
        INSERT INTO categories (id, name, color)
        VALUES  (1, "Work", "red"),
                (2, "Research", "cyan"),
                (3, "Study", "green"),
                (4, "Side Projects", "yellow"),
                (5, "Personal", "blue")
        ;
        """
    )
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


def create_database():

    create_tasks_table()
    create_categories_table()
    insert_default_categories()
    create_time_tracking_table()
    create_alarms_table()

    conn.commit()
    conn.close()
