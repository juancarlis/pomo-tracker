import typer
from src.categories.models import Category
from rich.console import Console
from rich.table import Table


from src.categories.service import get_all_categories


console = Console()
categories_app = typer.Typer()


@categories_app.command(short_help="show all categories")
def show():
    categories = get_all_categories()
    console.print("[bold magenta]Categories[/bold magenta]!", "📔")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Category", min_width=20)
    table.add_column("Color", min_width=15)

    for _, category in enumerate(categories, start=1):
        table.add_row(category.name, category.color)

    console.print(table)
