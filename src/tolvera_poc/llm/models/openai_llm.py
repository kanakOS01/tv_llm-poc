from openai import OpenAI
from ..load_env import OPENAI_API_KEY

from .base import BaseLLM

BASE_PROMPT = """You are a helpful assistant with knowledge about Tolvera. Tölvera is a Python library designed for composing together and interacting with basal agencies, inspired by fields such as artificial life (ALife) and self-organising systems. It provides creative coding-style APIs that allow users to combine and compose various built-in behaviours, such as flocking, slime mold growth, and swarming, and also author their own.
Your task is to generate tolvera code according to the user's query.

Example Tolvera code - 
import taichi as ti
from tolvera import Tolvera, run

def main(**kwargs):
    tv = Tolvera(**kwargs)

    @ti.kernel
    def draw():
        w = 100
        tv.px.rect(tv.x/2-w/2, tv.y/2-w/2, w, w, ti.Vector([1., 0., 0., 1.]))

    @tv.render
    def _():
        tv.p()
        draw()
        return tv.px

if __name__ == '__main__':
    run(main)"""

class OpenAILLM(BaseLLM):
    """OpenAI LLM provider."""

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            max_retries=2,
        )

    def generate(self, prompt):
        """Generate response using OpenAI API."""
        response = self.client.responses.create(
            model="gpt-4o-mini",
            instructions=BASE_PROMPT,
            input=prompt,
            stream=True
        )

        for event in response:
            if hasattr(event, "delta"):
                yield event.delta
