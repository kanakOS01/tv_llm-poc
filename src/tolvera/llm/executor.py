import subprocess
import sys


class CodeExecutor:
    """Helper class to execute AI generated code."""

    
    def __init__(self, code_path: str = "ai_generated_script.py"):
        self.code_path = code_path

    
    def save_code(self, code: str):
        """Save the code to a file."""
        with open(self.code_path, "w") as f:
            f.write(code)

    
    def execute_file(self):
        """Execute the file at 'code_path'."""
        try:
            res = subprocess.run(
                [sys.executable, self.code_path],
                capture_output=True,
                text=True,
            )
            return res.stdout or "Execution Complete. Check Visualizations."
        except Exception as e:
            return str(e)

    
    def save_and_execute(self, code: str):
        """Save and execute the code."""
        self.save_code(code)
        return self.execute_file()
    

if __name__ == "__main__":
    code_executor = CodeExecutor()
    code = """import taichi as ti
from tolvera import Tolvera, run

def main(**kwargs):
    tv = Tolvera(**kwargs)

    @ti.kernel
    def draw():
        width = 100
        height = 300
        tv.px.rect(tv.x/2 - width/2, tv.y/2 - height/2, width, height, ti.Vector([1., 0., 0., 1.]))

    @tv.render
    def _():
        tv.p()
        draw()
        return tv.px

if __name__ == '__main__':
    run(main)"""
    print(code_executor.save_and_execute(code))