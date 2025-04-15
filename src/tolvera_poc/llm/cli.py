import code
import openai
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from .models.openai_llm import OpenAILLM
from .executor import CodeExecutor

app = typer.Typer()
console = Console()
openai_llm = OpenAILLM()
code_executor = CodeExecutor()

USER_INSTRUCTIONS = """[bold cyan]Chat with Tolvera![/bold cyan]
        
[bold violet]Commands - [/bold violet]
    Type '[bold red]/run[/bold red]' to run the generated code.
    Type '[bold red]/clear[/bold red]' to clear screen.
    Type '[bold red]/exit[/bold red]' to quit."""


def get_code_from_response(response):
    code = ""
    if "```python" in response:
        code = response.split("```python")[1].split("```")[0]
    return code.strip()


@app.command()
def chat():
    """Chat with Tolvera in an interactive session."""
    console.print(Panel(USER_INSTRUCTIONS, style="green"))
    generated_code_snippets = []

    while True:
        response = ""
        try:
            user_input = Prompt.ask("\n[bold yellow]┃ You[/bold yellow]")

            if user_input.lower() == "/exit":
                console.print()
                console.print(Panel("[bold red]Goodbye![/bold red] 👋", style="bold magenta"))
                break

            elif user_input.lower() == "/clear":
                console.clear()
                console.print(Panel(USER_INSTRUCTIONS, style="green"))
                continue

            elif user_input.lower() == "/run":
                if not generated_code_snippets:
                    console.print("[bold red]No code snippets generated yet![/bold red]")
                    continue
                console.print("\n[bold green]Running the last generated code...[/bold green]")
                code = generated_code_snippets[-1]
                result = code_executor.save_and_execute(code)
                console.print(Markdown(result))
                continue

            # Generate LLM response
            console.print("\n[bold cyan]┃ Tolvera:[/bold cyan]", end=" ", style="bold cyan")
            for chunk in openai_llm.generate(user_input):
                console.print(chunk, end="")
                response += chunk
            console.print()

            # Extract code if present
            code_snippet = get_code_from_response(response)
            if code_snippet:
                generated_code_snippets.append(code_snippet)

        except KeyboardInterrupt:
            console.print("\n[bold red]Session interrupted. Exiting...[/bold red] 🚪")
            break
