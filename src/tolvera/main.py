import typer

from .llm.cli import app as llm_app

app = typer.Typer()

@app.command()
def tolvera():
    """CLI entry point for Tolvera."""
    pass

app.add_typer(llm_app)

if __name__ == "__main__":
    app()