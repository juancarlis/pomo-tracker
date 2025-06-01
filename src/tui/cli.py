import typer
from rich.console import Console


console = Console()
ui_app = typer.Typer(invoke_without_command=True)


@ui_app.callback()
def main(ctx: typer.Context):
    """
    Default command when `ui` is called withoud arguments.
    """
    if ctx.invoked_subcommand is None:
        start()


@ui_app.command()
def start():
    """Start ui"""
    from tui.app import TaskApp

    TaskApp().run()
