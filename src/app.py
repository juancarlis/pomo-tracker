import typer
from tasks.cli import task_app
from categories.cli import categories_app
from tracker.cli import tracker_app
from alarm.cli import alarm_app
from setup import setup_app
from utils.cli import utils_app

app = typer.Typer()


app.add_typer(task_app, name="task", help="Tasks management commands")
app.add_typer(categories_app, name="categories", help="Categories management commands")
app.add_typer(tracker_app, name="tracker", help="Tracker management commands")
app.add_typer(alarm_app, name="alarm", help="Standalone alarms")
app.add_typer(setup_app, name="setup", help="Setup and installation commands")
app.add_typer(utils_app, name="utils", help="Utility commands")
