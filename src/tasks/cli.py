from src.categories.service import get_all_categories, get_category_id_from_name
from src.tasks.models import Task
import typer
from rich.console import Console
from rich.table import Table

from src.tasks.service import (
    get_all_tasks,
    delete_task,
    insert_task,
    complete_task,
    update_task,
)


console = Console()
task_app = typer.Typer()


@task_app.command(short_help="add an item")
def add(task_description: str, category: str):
    category_id = get_category_id_from_name(category)
    if category_id is None:
        typer.echo(
            f"Category {category} does not exists. Use `taskcli categories show` to see available."
        )
        return
    typer.echo(f"adding {task_description}, {category}")
    task = Task(description=task_description, category_id=category_id)
    insert_task(task)
    show()


@task_app.command()
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_task(position - 1)
    show()


@task_app.command()
def update(position: int, task_description: str = "", category: str = ""):
    typer.echo(f"updating {position}")
    update_task(position - 1, task_description, category)
    show()


@task_app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_task(position - 1)
    show()


@task_app.command()
def show():
    tasks = get_all_tasks()
    console.print("[bold magenta]Tasks[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category_id)
        is_done_str = "✅" if task.status == 1 else "❌"
        table.add_row(
            str(idx), task.description, f"[{c}]{task.category_id}[/{c}]", is_done_str
        )

    console.print(table)


def get_category_color(category):
    """Returns category color"""
    categories = {category.name: category.color for category in get_all_categories()}
    return categories.get(category, "white")


if __name__ == "__main__":
    task_app()
