import csv
from typing import Any, List
from database import get_connection


def export_table_to_csv(table_name: str, csv_path: str) -> None:
    """
    Export an entire SQLite table to a csv file.

    Args:
        table_name (str): Name of the table to export.
        csv_path (str): Destination file path for the CSV.
    """
    conn = get_connection()
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table_name}")
    rows: List[tuple[Any]] = c.fetchall()

    column_names = [description[0] for description in c.description]

    with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(column_names)
        writer.writerows(rows)

    conn.close()
