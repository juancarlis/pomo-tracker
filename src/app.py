import typer
from src.tasks.cli import task_app
from src.categories.cli import categories_app
from src.tracker.cli import tracker_app

app = typer.Typer()


app.add_typer(task_app, name="task", help="Tasks management commands")
app.add_typer(categories_app, name="categories", help="Categories management commands")
app.add_typer(tracker_app, name="tracker", help="Tracker management commands")
