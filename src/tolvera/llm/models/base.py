from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Base class for all LLM providers."""
    
    def __init__(self, **kwargs):
        self.params = kwargs
        self.model = None
        self.tokenizer = None
        self.device = None
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text based on the provided prompt."""
        pass

    