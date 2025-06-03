import os
import tempfile
import subprocess

from loguru import logger
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Input, Label
from textual.reactive import reactive
from textual.screen import Screen
from textual.message import Message

from tasks.service import (
    delete_task,
    get_pending_tasks,
    complete_task,
    insert_task,
    insert_task_content,
    update_task_content,
    get_task_content,
)
from tracker.service import insert_time_tracking, stop_time_tracking
from categories.service import get_category_id_from_name_or_id
from tasks.models import Task
from settings import settings


logger.remove()
logger.add(
    "app.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time: YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


class AddTaskScreen(Screen):
    BINDINGS = [
        ("escape", "close_modal", "Close"),
    ]

    class TaskData(Message):

        def __init__(self, title: str, category: str) -> None:
            super().__init__()
            self.title = title
            self.category = category

    def compose(self) -> ComposeResult:
        yield Label("➤ Nuevo Task", id="add_label")
        yield Input(placeholder="Task title", id="title_input")

        yield Input(
            placeholder=f"Category (default: {settings.default_category})",
            id="category_input",
        )

    def on_mount(self) -> None:
        self.query_one("#title_input", Input).focus()

    def action_close_modal(self) -> None:
        self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Triggered when the user presses Enter in an Input.
        - If it is the title_input → moves focus to the category_input.
        - If it is the category_input → creates the task and closes the modal.
        """
        widget_id = event.input.id
        if widget_id == "title_input":
            self.query_one("#category_input", Input).focus()
            return

        if widget_id == "category_input":
            # Read title and category, publish message and closes
            title_widget = self.query_one("#title_input", Input)
            category_widget = self.query_one("#category_input", Input)

            title = title_widget.value.strip()
            category = category_widget.value.strip() or settings.default_category

            self.post_message(AddTaskScreen.TaskData(title, category))

            self.app.pop_screen()
            return


class TaskApp(App):

    selected_row = reactive(0)

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
        ("a", "show_add_screen", "Add task"),
        ("d", "delete_task", "Delete task"),
        ("c", "complete_task", "Complete task"),
        ("e", "edit_content", "Edit content"),
        ("r", "refresh_tasks", "Update"),
        ("t", "toggle_tracking", "Toggle tracking"),
    ]

    def on_load(self) -> None:
        user_theme = os.getenv("GLOBAL_THEME", "dark").lower()
        logger.info(f"Theme: {user_theme}")
        if user_theme == "light":
            self.theme = "solarized-light"
        else:
            self.theme = "nord"

    def compose(self) -> ComposeResult:
        yield Header()
        self.table = DataTable(zebra_stripes=True)
        yield self.table
        yield Footer()

    def on_mount(self):
        self.load_tasks()

    def load_tasks(self):
        tasks = get_pending_tasks()
        self.table.clear(columns=True)
        self.table.add_columns("#", "Task", "Category", "Date Added", "Tracking")

        for task in tasks:
            tracking = "▶" if task.tracking else ""
            self.table.add_row(
                str(task.position),
                task.title,
                task.category_name,
                task.date_added,
                tracking,
            )

        if self.table.row_count:
            row = min(self.selected_row, self.table.row_count - 1)
        else:
            row = 0

        self.table.cursor_type = "row"
        self.table.focus()
        self.table.cursor_coordinate = (row, 0)

    def action_cursor_down(self):
        row, col = self.table.cursor_coordinate
        if row < self.table.row_count - 1:
            new = row + 1
            self.table.cursor_coordinate = (new, col)
            self.selected_row = new

    def action_cursor_up(self):
        row, col = self.table.cursor_coordinate
        if row > 0:
            new = row - 1
            self.table.cursor_coordinate = (new, col)
            self.selected_row = new

    def action_show_add_screen(self) -> None:
        self.push_screen(AddTaskScreen())

    def on_add_task_screen_task_data(self, message: AddTaskScreen.TaskData) -> None:
        logger.info("Adding task with tui")

        title = message.title
        category_name = message.category

        category_id = get_category_id_from_name_or_id(category_name)
        if category_id is None:
            category_id = get_category_id_from_name_or_id(settings.default_category)

        new = Task(title=title, category_id=category_id)
        insert_task(new)

        self.selected_row = self.table.row_count
        self.load_tasks()

    def action_delete_task(self):
        """
        d -> Soft deletes the selected task
        """
        logger.info("Deleting task with tui")
        if self.table.row_count == 0:
            return

        row_index, _ = self.table.cursor_coordinate
        row = self.table.get_row_at(row_index)
        task_pos = int(row[0])
        delete_task(task_pos)

        self.selected_row = row_index
        self.load_tasks()

    def action_complete_task(self):
        """
        c -> Completes the selected task
        """
        logger.info("Completing task with tui")

        if self.table.row_count == 0:
            return

        row_index, _ = self.table.cursor_coordinate
        row = self.table.get_row_at(row_index)
        task_pos = int(row[0])
        complete_task(task_pos)

        self.selected_row = row_index
        self.load_tasks()

    def action_edit_content(self):
        """
        e -> Opens editor to write content
        """

        if not self.table.row_count:
            return

        row_index, _ = self.table.cursor_coordinate
        pos = int(self.table.get_row_at(row_index)[0])
        logger.info(f"Editing task content at position {pos}")

        current_content = get_task_content(pos) or ""

        with tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, mode="w+", encoding="utf-8"
        ) as tmp:
            tmp.write(current_content)
            tmp.flush()
            tmp_path = tmp.name

        editor = os.environ.get("EDITOR", "nvim")
        subprocess.call([editor, tmp_path])

        with open(tmp_path, "r", encoding="utf-8") as f:
            new_content = f.read()
        os.unlink(tmp_path)

        if current_content:
            update_task_content(pos, new_content)
            logger.info(f"Task {pos} content updated.")
        else:
            insert_task_content(pos, new_content)
            logger.info(f"Task {pos} content created")

        self.exit()

    def action_toggle_tracking(self):
        """
        t -> Toggle time tracking on the selected task
        """
        logger.info("Toggling time tracking with tui")
        if self.table.row_count == 0:
            return

        row_index, _ = self.table.cursor_coordinate

        row = self.table.get_row_at(row_index)
        task_pos, tracking = int(row[0]), row[4]

        logger.info("jaja")
        logger.info(f"Tarea pos {task_pos}, esta track {tracking}")

        if tracking == "":
            logger.info("Bien")
            insert_time_tracking(task_pos)
        else:
            logger.info("Mal")
            stop_time_tracking(task_pos)

        self.selected_row = row_index
        self.load_tasks()

    def action_refresh_tasks(self):
        self.load_tasks()


if __name__ == "__main__":
    TaskApp().run()
