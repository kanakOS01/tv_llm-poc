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
        """Generate AI response."""
        pass


    @abstractmethod
    def generate_with_streaming(self, prompt: str):
        """Generate AI response with streaming."""
        pass