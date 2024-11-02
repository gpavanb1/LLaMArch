from typing import Optional, Dict, Any, List


class LLM:
    def __init__(self,
                 model_category: str,
                 model_name: str,
                 api_key: Optional[str] = None,
                 model_parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize the LLM client and (optionally) a separate embedding model based on specified names.

        Args:
            model_category (str): The name of the language model provider (e.g., 'openai', 'huggingface', 'cohere').
            model_name (str): The name of the model
            api_key (str): Optional, The API key for the selected provider.
            model_parameters (dict): Optional, Additional parameters for model configuration.
        """
        self.model_category = model_category.lower()
        self.model_name = model_name.lower() if model_name else None
        self.api_key = api_key
        self.model_parameters = model_parameters or {}

        # Initialize the language model and embedding model
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the language model based on the specified category."""
        if self.model_category == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                openai_api_key=self.api_key,
                model_name=self.model_name or "gpt-3.5-turbo",
                **self.model_parameters
            )
        elif self.model_category == "huggingface":
            from langchain_huggingface import HuggingFacePipeline
            return HuggingFacePipeline.from_model_id(
                model_id=self.model_name,
                task="text-generation",
                **self.model_parameters
            )
        elif self.model_category == "cohere":
            from langchain_community.llms import Cohere
            return Cohere(
                cohere_api_key=self.api_key,
                model=self.model_name,
                **self.model_parameters
            )
        else:
            raise ValueError(
                f"Unsupported model category: {self.model_category}")

    def generate(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """
        Generate a response from the language model.

        Args:
            prompt (str): The input prompt for the LLM.
            max_tokens (int): Maximum number of tokens for the response.
            temperature (float): The temperature parameter for controlling randomness.

        Returns:
            str: Generated text from the LLM.
        """
        response = self.llm.invoke(
            prompt,
            config={
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )
        return response.content if hasattr(response, 'content') else response
