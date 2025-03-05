from datetime import datetime
from src.alarm.service import (
    get_active_alarms,
    insert_alarm,
    start_alarm_process,
    stop_alarm_by_id,
    stop_all_alarms,
)
import typer
from rich.console import Console


console = Console()
alarm_app = typer.Typer(invoke_without_command=True)

RECURRING_DEFAULT = False


@alarm_app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        list()


@alarm_app.command(short_help="Start a standalone alarm")
def start(duration: int, recurring: bool = RECURRING_DEFAULT):
    """
    Initiates an alarm of `duration` minutes.
    """

    active_alarms = get_active_alarms()
    if active_alarms:
        console.print(
            f"[bold yellow]⚠️ Active alarm: {active_alarms[0][0]} (ends at {active_alarms[0][2]})[/bold yellow]"
        )

    alarm_id, end_time = insert_alarm(duration, recurring)

    typer.echo(f"Alarm {alarm_id} set in {duration} minutes.")

    start_alarm_process()


@alarm_app.command(short_help="Stop an alarm")
def stop(alarm_id: int):
    stop_alarm_by_id(alarm_id)
    console.print(f"🔕 Alarm {alarm_id} stopped.")


@alarm_app.command(short_help="Stop all alarms.")
def stop_all():
    stop_all_alarms()
    console.print("🔕 All alarms stopped.")


@alarm_app.command(short_help="List active alarms")
def list():
    """Shows active alarms with remaining duration."""

    alarms = get_active_alarms()

    if not alarms:
        console.print("[bold yellow]⚠️ No active alarms were found.[/bold yellow]")
        return

    console.print("[bold cyan]⏰ Active alarms:[/bold cyan]")
    for alarm_id, duration, end_time, recurring in alarms:
        end_time_dt = datetime.fromisoformat(end_time)
        time_left = max(
            0, (datetime.fromisoformat(end_time) - datetime.now()).total_seconds() // 60
        )
        status = "🔁 Recurring" if recurring else "✅ One-time"
        formatted_end_time = end_time_dt.strftime("%H:%M:%S")
        console.print(
            f"🔔 Alarm {alarm_id}: ends at {formatted_end_time}, {duration} min (left {int(time_left)} min [{status}])"
        )


def clean():
    from src.alarm.service import clean_finished_alarms

    clean_finished_alarms()
    console.print("[bold green]Finished alarms deleted.[/bold green]")


if __name__ == "__main__":
    alarm_app()
