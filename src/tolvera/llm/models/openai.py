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
            instructions="""You""",
            input=prompt,
            stream=True
        )

        return response.output_text