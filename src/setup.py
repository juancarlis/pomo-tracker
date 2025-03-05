import typer
import subprocess
from src.init_db import create_database

setup_app = typer.Typer()


@setup_app.command(short_help="Initialize the database and install dependencies.")
def install():
    """Installs dependencies and sets up the database."""
    typer.echo("📦 Creating the database...")
    create_database()
    typer.echo("✅ Installation completed. Run `taskcli show` to start using it.")


@setup_app.command(short_help="Seed the database with sample tasks.")
def seed():
    """Inserts sample tasks into the database."""
    tasks = [
        "Review financial report",
        "Write an AI article",
        "Study linear algebra",
        "Optimize side project code",
        "Plan vacation trip",
        "Prepare client presentation",
        "Read ML research paper",
        "Solve statistics exercises",
        "Implement new feature",
        "Organize personal files",
    ]
    categories = [1, 2, 3, 4, 5]  # Category IDs

    for task in tasks:
        category = str(categories[tasks.index(task) % len(categories)])
        typer.echo(f"➕ Adding task: '{task}' in category {category}...")
        subprocess.run(["taskcli", "task", "add", task, category], check=True)

    typer.echo("✅ Sample tasks added successfully.")
