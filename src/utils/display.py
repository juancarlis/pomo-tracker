from rich.console import Console
from rich.table import Table
from typing import Any, Callable, Dict, List, Tuple, Optional

console = Console()


def display_table(
    title: str,
    columns: List[str],
    rows: List[Tuple],
    column_styles: Optional[List[str]] = None,
    column_formatters: Optional[Dict[int, Callable[[Any], str]]] = None,
    emoji: str = "",
):
    """
    Generic function to display a table with rich.

    Args:
        title (str): The title of the table.
        columns (List[str]): Column names.
        rows (List[Tuple]): List of tuples, where each tuple represents a row.
        column_styles (Optional[List[str]]): Styles for each column (e.g., "dim", "bold").
    """

    if emoji == "":
        emoji = "📊"

    console.print(f"[bold magenta]{title}[/bold magenta]", f"{emoji}")

    table = Table(show_header=True, header_style="bold blue")

    for idx, col in enumerate(columns):
        style = column_styles[idx] if column_styles and idx < len(column_styles) else ""
        table.add_column(col, style=style)

    for row in rows:
        formatted_row = [
            (
                column_formatters[idx](value)
                if column_formatters and idx in column_formatters
                else str(value)
            )
            for idx, value in enumerate(row)
        ]
        table.add_row(*formatted_row)

    console.print(table)
