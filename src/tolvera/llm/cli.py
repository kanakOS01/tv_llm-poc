import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text


app = typer.Typer()
console = Console()


@app.command()
def chat():
    """Chat with Tolvera in an interactive session."""
    console.print(Panel(
        """[bold cyan]Chat with Tolvera![/bold cyan]
        
[bold violet]Commands - [/bold violet]
    Type '[bold red]/run[/bold red]' to run the generated code.
    Type '[bold red]/clear[/bold red]' to clear screen.
    Type '[bold red]/exit[/bold red]' to quit.""", 
        style="green")
    )
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold yellow]┃ You[/bold yellow]")  # Get user input
            
            if user_input.lower() == "/exit":
                console.print()
                console.print(Panel("[bold red]Goodbye![/bold red] 👋", style="bold magenta"))
                break
            
            response = """**Tolvera** is a Python library designed for composing and interacting with basal agencies.  
It is inspired by **artificial life (ALife)** and **self-organizing systems**, allowing users to create complex simulations with simple rules.

Example usage:  
```python
from tolvera import Tolvera, run

def main(**kwargs):
    tv = Tolvera(**kwargs)
    tv.run()
```"""
            
            # Display response inside a panel with markdown formatting
            console.print("\n[bold cyan]┃ Tolvera:[/bold cyan]", end=" ", style="bold cyan")
            console.print(Markdown(response)) 

        except KeyboardInterrupt:
            console.print("\n[bold red]Session interrupted. Exiting...[/bold red] 🚪")
            break
