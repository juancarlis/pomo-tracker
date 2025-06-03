DDL_CREATE_TASKS_TABLE = """
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


DDL_CREATE_CATEGORIES_TABLE = """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        color TEXT
    );
"""

INSERT_DEFAULT_CATEGORIES = """
    INSERT INTO categories (id, name, color)
    VALUES  (1, "Inbox", "bright_black"),
            (2, "Work", "red"),
            (3, "Research", "cyan"),
            (4, "Study", "green"),
            (5, "Side Projects", "yellow"),
            (6, "Personal", "blue"),
            (7, "Focus work", "dodger_blue_3"),
            (8, "Light work", "bright_yellow"),
            (9, "Hotfix", "bright_red"),
            (10, "Request", "dark_orange")
    ;
"""

DDL_CREATE_TASKS_CONTENT_TABLE = """
    CREATE TABLE IF NOT EXISTS tasks_contents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (task_id) REFERENCES tasks(id)
    );
"""
