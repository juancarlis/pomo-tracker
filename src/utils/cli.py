from pathlib import Path

import typer
from rich.console import Console

from utils.export_csv import export_table_to_csv


console = Console()
utils_app = typer.Typer()


@utils_app.command(short_help="export table")
def export(table: str, path: Path = typer.Option(None, help="Output CSV path")):
    """
    Export specified table to CSV.

    Args:
        table (str): The database table to export.
        path (Path, optional): Path to the CSV file. Defaults to <table>.csv in current directory.
    """

    if path is None:
        path = Path(f"{table}.csv")

    try:
        export_table_to_csv(table, str(path))
        typer.echo(f"✅ Exported {table} table succesfully to {path}.")
    except Exception as e:
        typer.echo(f"❌ Error exporting {table}: {e}", err=True)
