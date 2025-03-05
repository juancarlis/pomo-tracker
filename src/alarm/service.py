import subprocess
from datetime import datetime, timedelta
from src.database import get_connection

conn = get_connection()
c = conn.cursor()


def start_alarm_process():
    subprocess.Popen(
        ["python3", "src/alarm/check_alarms.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def insert_alarm(duration: int, recurring: bool):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration)

    with conn:
        c.execute(
            """
            INSERT INTO alarms (duration, start_time, end_time, status, recurring)
            VALUES (?, ?, ?, 'pending', ?)
            """,
            (duration, start_time.isoformat(), end_time.isoformat(), int(recurring)),
        )
        alarm_id = c.lastrowid

    return alarm_id, end_time.isoformat()


def get_active_alarms():
    c.execute(
        """
    SELECT
        id,
        duration,
        end_time,
        recurring
    FROM alarms
    WHERE status = 'pending'
    """
    )
    return c.fetchall()


def mark_alarm_as_finished(alarm_id: int):
    with conn:
        c.execute("UPDATE alarms SET status = 'finished' WHERE id = ?", (alarm_id,))


def stop_alarm_by_id(alarm_id: int):
    """Marca una alarma como detenida."""
    with conn:
        c.execute("UPDATE alarms SET status = 'stopped' WHERE id = ?", (alarm_id,))


def stop_all_alarms():
    """Marca todas las alarmas activas como detenidas."""
    with conn:
        c.execute("UPDATE alarms SET status = 'stopped'")


def clean_finished_alarms():
    with conn:
        c.execute("DELETE FROM alarms WHERE status = 'finished'")
