import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.status import Status

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
        try:
            console.print()  # Single newline at the start of each interaction
            user_input = Prompt.ask("[bold yellow]┃ You[/bold yellow]")
            console.print()

            match user_input.lower():
                case "/exit":
                    console.print(Panel("[bold red]Goodbye![/bold red] 👋", style="bold magenta"))
                    break

                case "/clear":
                    console.clear()
                    console.print(Panel(USER_INSTRUCTIONS, style="green"))
                    continue

                case "/run":
                    if not generated_code_snippets:
                        console.print("[bold red]No code snippets generated yet![/bold red]")
                        continue
                    console.print("[bold green]Running the last generated code...[/bold green]")
                    code = generated_code_snippets[-1]
                    with console.status("[bold green]Running your code...[/bold green]", spinner="dots"):
                        result = code_executor.save_and_execute(code)
                    console.print(Markdown(result))
                    continue

            # Generate LLM response
            # console.print("\n[bold cyan]┃ Tolvera:[/bold cyan]", end=" ", style="bold cyan")
            # for chunk in openai_llm.generate(user_input):
            #     console.print(chunk, end="")
            #     response += chunk
            # console.print()
            with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots10"):
                response = openai_llm.generate(user_input).strip()

            console.print("[bold cyan]┃ Tolvera:[/bold cyan]", end=" ")
            console.print(Markdown(response), end="")

            # Extract code if present
            code_snippet = get_code_from_response(response)
            if code_snippet:
                generated_code_snippets.append(code_snippet)

        except KeyboardInterrupt:
            console.print("\n[bold red]Session interrupted. Exiting...[/bold red] 🚪")
            break
