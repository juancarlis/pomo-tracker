import time
import subprocess
from datetime import datetime

from rich.console import Console

from src.alarm.service import get_active_alarms, mark_alarm_as_finished


console = Console()
NOTIFY_EVERY = 120


def notify_user(message: str):
    try:
        subprocess.run(["wsl-notify-send.exe", message], check=True)
    except FileNotFoundError:
        console.print(
            f"[bold red]{message} (Instala wsl-notify-send para recibir notificaciones.)"
        )


def check_and_trigger_alarms():
    while True:
        alarms = get_active_alarms()
        now = datetime.now()

        if not alarms:
            break

        for alarm_id, duration, end_time, recurring in alarms:
            end_time_dt = datetime.fromisoformat(end_time)

            if end_time_dt <= now:
                notify_user(f"⏰ Alarm {alarm_id}: {duration} min time elapsed!")

                if recurring:
                    time.sleep(NOTIFY_EVERY)
                else:
                    mark_alarm_as_finished(alarm_id)

        time.sleep(10)


if __name__ == "__main__":
    console.print("[bold green]🔄 Alarm checker running...[/bold green]")
    check_and_trigger_alarms()
