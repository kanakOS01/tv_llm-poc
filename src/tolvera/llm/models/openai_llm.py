from openai import OpenAI
from ..load_env import OPENAI_API_KEY

from .base import BaseLLM

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
            instructions="""You are a helpful assistant with knowledge about Tolvera. Tölvera is a Python library designed for composing together and interacting with basal agencies, inspired by fields such as artificial life (ALife) and self-organising systems. It provides creative coding-style APIs that allow users to combine and compose various built-in behaviours, such as flocking, slime mold growth, and swarming, and also author their own.

Your task is to generate tolvera code according to the user's query.""",
            input=prompt,
            stream=True
        )

        for event in response:
            if hasattr(event, "delta"):
                yield event.delta
