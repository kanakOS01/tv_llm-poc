import typer

from .cli import app as llm_app

app = typer.Typer()

app.add_typer(llm_app)