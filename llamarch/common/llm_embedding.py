from typing import Optional, Dict, Any, List


class LLMEmbedding:
    def __init__(self,
                 model_category: str,
                 embedding_model_name: str,
                 api_key: Optional[str] = None,
                 model_parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize the LLM embedding client and (optionally) a separate embedding model based on specified names.

        Args:
            model_category (str): The name of the language model provider (e.g., 'openai', 'huggingface', 'cohere').
            embedding_model_name (str): The name of the embedding model.
            api_key (str): Optional, The API key for the selected provider.
            model_parameters (dict): Additional parameters for model configuration.
        """
        self.model_category = model_category.lower()
        self.embedding_model_name = embedding_model_name.lower(
        ) if embedding_model_name else None
        self.api_key = api_key
        self.model_parameters = model_parameters or {}

        # Initialize the language model and embedding model
        self.embedding_model = self._initialize_embeddings()

    def _initialize_embeddings(self):
        """Initialize the embedding model based on the specified category."""
        if self.model_category == "openai":
            from langchain_openai import OpenAIEmbeddings  # New import in 0.3
            return OpenAIEmbeddings(
                openai_api_key=self.api_key,
                model=self.embedding_model_name or "text-embedding-ada-002"
            )
        elif self.model_category == "huggingface":
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(
                model_name=self.embedding_model_name,
                encode_kwargs={"device": "cpu", "batch_size": 32}
            )
        elif self.model_category == "cohere":
            from langchain_community.embeddings import CohereEmbeddings
            return CohereEmbeddings(
                cohere_api_key=self.api_key,
                model=self.embedding_model_name
            )
        else:
            raise ValueError(
                f"Unsupported model category: {self.model_category}")

    def get_embeddings(self, text: str) -> List[float]:
        """
        Get embeddings for a given text using the specified embedding model.

        Args:
            text (str): The input text for which embeddings are needed.

        Returns:
            List[float]: Embedding vector for the input text.
        """
        return self.embedding_model.embed_query(text)
