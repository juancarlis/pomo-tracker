from typing import List, Optional
from datetime import date, timedelta

from utils.display import display_table
import typer

from tasks.cli import get_category_color
from rich.console import Console
from rich.table import Table

from tracker.service import (
    get_active_timer,
    get_daily_summary,
    insert_time_tracking,
    stop_time_tracking,
)
from tracker.models import ActiveTimer, DailySummary
from alarm.cli import start as start_alarm

console = Console()
tracker_app = typer.Typer(invoke_without_command=True)

RECURRING_DEFAULT_IN_TIMER = True


@tracker_app.callback()
def main(ctx: typer.Context):
    """
    Default command when `tracker` is called without arguments.
    """
    if ctx.invoked_subcommand is None:
        active()


@tracker_app.command(short_help="Start time tracking for a task")
def start(
    task_id: int,
    timer: int = typer.Option(None, help="Set a timer in minutes"),
    recurring: bool = RECURRING_DEFAULT_IN_TIMER,
):
    """
    Starts tracking a task
    """
    insert_time_tracking(task_id)

    if timer:
        start_alarm(duration=timer, recurring=recurring)

    console.print(
        f"[bold green]✅ Task tracking started for task {task_id}.[/bold green]"
    )


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
    table.add_column("Elapsed [HH:MM:SS]")

    c = get_category_color(active_timer.category)
    table.add_row(
        str(active_timer.position),
        active_timer.task,
        f"[{c}]{active_timer.category}[/{c}]",
        active_timer.start_time.strftime("%Y-%m-%d %H:%M"),
        active_timer.current_time.strftime("%Y-%m-%d %H:%M"),
        active_timer.elapsed_time,
    )
    console.print(table)


@tracker_app.command(short_help="Daily summary")
def summary(
    search_date: Optional[str] = typer.Option(
        None, "--date", "-d", help="Fetch data for a specific date (YYYY-MM-DD)"
    ),
    relative: int = typer.Option(
        0, "--relative", "-r", help="Relative days offset (e.g., -1 for yesterday)"
    ),
):

    try:
        summary = get_daily_summary(date_str=search_date, relative_days=relative)
    except ValueError as e:
        console.print(f"[bold red]{e}[/bold red]")
        raise typer.Exit(1)

    if summary is None:
        console.print("[bold red]No tracking data found.[/bold red]")
        return

    rows = [
        (
            row.id,
            row.task,
            row.category,
            row.minutes_elapsed,
            row.hours_elapsed,
            row.start_time,
            row.end_time,
        )
        for row in summary
    ]

    display_table(
        title="Daily summary",
        columns=[
            "#",
            "Task",
            "Category",
            "Elapsed min",
            "Elapsed hrs",
            "Start time",
            "End time",
        ],
        rows=rows,
        column_styles=["dim", "dim", "", "dim", "dim", "dim", "dim"],
        column_formatters={
            2: lambda category: f"[{get_category_color(category)}]{category}[/{get_category_color(category)}]"
        },
        emoji="⌛",
    )
    return 0


if __name__ == "__main__":
    tracker_app()
