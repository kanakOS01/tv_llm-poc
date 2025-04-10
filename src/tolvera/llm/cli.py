import openai
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from .models.openai_llm import OpenAILLM

app = typer.Typer()
console = Console()
openai_llm = OpenAILLM()

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
    
    response = ""
    while True:
        try:
            user_input = Prompt.ask("\n[bold yellow]┃ You[/bold yellow]")
            
            if user_input.lower() == "/exit":
                console.print()
                console.print(Panel("[bold red]Goodbye![/bold red] 👋", style="bold magenta"))
                break
            
            
            console.print("\n[bold cyan]┃ Tolvera:[/bold cyan]", end=" ", style="bold cyan")
            for chunk in openai_llm.generate(user_input):
                console.print(chunk, end="")

            
            # console.print(response)

        except KeyboardInterrupt:
            console.print("\n[bold red]Session interrupted. Exiting...[/bold red] 🚪")
            break
