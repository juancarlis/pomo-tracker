import os
import tempfile
import subprocess

from categories.service import get_all_categories, get_category_id_from_name
from tasks.models import Task
from utils.date_funcs import format_date_to_min
from utils.display import display_table
import typer
from rich.console import Console
from rich.table import Table

from settings import settings
from tasks.service import (
    get_all_tasks,
    delete_task,
    get_pending_tasks,
    get_task_content,
    get_task_id_from_position,
    insert_task,
    complete_task,
    insert_task_content,
    update_task,
    update_task_content,
)


console = Console()
task_app = typer.Typer(invoke_without_command=True)


@task_app.callback()
def main(ctx: typer.Context):
    """
    Default command when `task` is called without arguments.
    """
    if ctx.invoked_subcommand is None:
        pending()


@task_app.command(short_help="add an item")
def add(title: str, category: str = typer.Argument(None)):

    if not category:
        category = settings.default_category

    category_id = get_category_id_from_name(category)
    if category_id is None:
        typer.echo(
            f"Category {category} does not exists. Use `taskcli categories show` to see available."
        )
        return
    typer.echo(f"adding {title}, {category}")
    task = Task(title=title, category_id=category_id)
    insert_task(task)
    show()


@task_app.command()
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_task(position)
    show()


@task_app.command()
def update(position: int, title: str = "", category: str = ""):
    typer.echo(f"updating {position}")
    update_task(position, title, category)
    show()


@task_app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_task(position)
    show()


@task_app.command()
def show():
    """Show all tasks."""

    tasks = get_all_tasks()

    if not tasks:
        console.print("[bold red]No pending tasks found.[/bold red]")

    console.print("[bold magenta]Tasks[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("id", style="dim", width=6)
    table.add_column("Task", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Date Added", min_width=12, justify="center")
    table.add_column("Date Completed", min_width=12, justify="center")
    table.add_column("#", style="dim", width=6, justify="center")
    table.add_column("Done", min_width=12, justify="right")

    for _, task in enumerate(tasks, start=1):
        c = get_category_color(task.category_id)
        is_done_str = "✅" if task.status == 1 else "❌"
        table.add_row(
            str(task.id),
            task.title,
            f"[{c}]{task.category_id}[/{c}]",
            format_date_to_min(task.date_added),
            format_date_to_min(task.date_completed),
            str(task.position),
            is_done_str,
        )

    console.print(table)


@task_app.command()
def pending():
    """Show pending tasks."""

    tasks = get_pending_tasks()
    if not tasks:
        console.print("[bold red]No pending tasks found.[/bold red]")

    rows = [
        (
            task.position,
            task.title,
            task.category_name,
            format_date_to_min(task.date_added),
            "⌚" if task.tracking else "",
        )
        for task in tasks
    ]

    display_table(
        title="Tasks",
        columns=["#", "Task", "Category", "Date Added", "Tracking"],
        rows=rows,
        column_styles=["dim", "dim", "", "dim", ""],
        column_formatters={
            2: lambda category: f"[{get_category_color(category)}]{category}[/{get_category_color(category)}]"
        },
        emoji="⌛",
    )
    return 0


@task_app.command("edit-content")
def edit_content(position: int):
    """Edit task content $EDITOR."""
    task_id = get_task_id_from_position(position)
    if task_id is None:
        typer.echo(f"No task found at position {position}.")
        raise typer.Exit(1)

    current_content = get_task_content(task_id) or ""

    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w+") as tmp:
        tmp.write(current_content)
        tmp.flush()
        tmp_path = tmp.name

    editor = os.environ.get("EDITOR", "nvim")
    subprocess.call([editor, tmp_path])

    with open(tmp_path, "r", encoding="utf-8") as f:
        new_content = f.read()

    os.unlink(tmp_path)

    if current_content:
        update_task_content(task_id, new_content)
        typer.echo("Content updated.")
    else:
        insert_task_content(task_id, new_content)
        typer.echo("Content created.")


def get_category_color(category):
    """Returns category color"""
    categories = {category.name: category.color for category in get_all_categories()}
    return categories.get(category, "white")


if __name__ == "__main__":
    task_app()
