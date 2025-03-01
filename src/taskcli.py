from src.model import Task
import typer
from rich.console import Console
from rich.table import Table

from src.database import (
    get_all_tasks,
    delete_task,
    insert_task,
    complete_task,
    update_task,
)


console = Console()
app = typer.Typer()


@app.command(short_help="add an item")
def add(task_description: str, category: str):
    typer.echo(f"adding {task_description}, {category}")
    task = Task(task_description, category)
    insert_task(task)
    show()


@app.command()
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_task(position - 1)
    show()


@app.command()
def update(position: int, task_description: str = "", category: str = ""):
    typer.echo(f"updating {position}")
    update_task(position - 1, task_description, category)
    show()


@app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_task(position - 1)
    show()


@app.command()
def show():
    tasks = get_all_tasks()
    console.print("[bold magenta]Tasks[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "✅" if task.status == 1 else "❌"
        table.add_row(
            str(idx), task.description, f"[{c}]{task.category}[/{c}]", is_done_str
        )

    console.print(table)


def get_category_color(category):
    COLORS = {"Learn": "cyan", "YouTube": "red", "Sports": "cyan", "Study": "green"}
    if category in COLORS:
        return COLORS[category]
    return "white"


if __name__ == "__main__":
    app()
