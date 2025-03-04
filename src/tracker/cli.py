from typing import Optional
from src.tasks.cli import get_category_color
import typer
from rich.console import Console
from rich.table import Table

from src.tracker.service import (
    get_active_timer,
    insert_time_tracking,
    stop_time_tracking,
)
from src.tracker.models import ActiveTimer

console = Console()
tracker_app = typer.Typer(invoke_without_command=True)


@tracker_app.callback()
def main(ctx: typer.Context):
    """
    Default command when `tracker` is called without arguments.
    """
    if ctx.invoked_subcommand is None:
        active()


@tracker_app.command(short_help="Start time tracking for a task")
def start(task_id: int):
    """
    Starts tracking a task
    """
    typer.echo(f"⏳ Timer starts for task {task_id}...")
    insert_time_tracking(task_id)


@tracker_app.command(short_help="Stop time tracking a task")
def stop(task_id: int):
    """
    Stops time tracking a task
    """
    stop_time_tracking(task_id)
    typer.echo(f"Timer stopped for {task_id}.")


@tracker_app.command(short_help="Active timer")
def active():
    """
    Fetch active timers
    """
    active_timer: Optional[ActiveTimer] = get_active_timer()

    if active_timer is None:
        console.print("[bold red]No active timers.[/bold red]")
        return

    console.print("[bold magenta]Active Timer[/bold magenta]", "⌛")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Task", style="dim", min_width=15)
    table.add_column("Category", min_width=12)
    table.add_column("Start Time")
    table.add_column("Current Time")
    table.add_column("Elapsed (sec)")
    table.add_column("Elapsed (min)")

    c = get_category_color(active_timer.category)
    table.add_row(
        str(active_timer.position),
        active_timer.task,
        f"[{c}]{active_timer.category}[/{c}]",
        active_timer.start_time.isoformat(),
        active_timer.current_time.isoformat(),
        str(round(active_timer.elapsed_time_seconds, 2)),
        str(round(active_timer.elapsed_time_minutes, 2)),
    )
    console.print(table)


if __name__ == "__main__":
    tracker_app()
