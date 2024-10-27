from langchain.llms import OpenAI, HuggingFaceHub, Cohere
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings, CohereEmbeddings


class LLM:
    def __init__(self, model_name="openai", api_key=None, embedding_model_name=None, model_parameters=None):
        """
        Initialize the LLM client and (optionally) a separate embedding model based on specified names.

        Args:
            model_name (str): The name of the language model provider (e.g., 'openai', 'huggingface', 'cohere').
            api_key (str): The API key for the selected provider.
            embedding_model_name (str): Optional; the name of the embedding model provider (if different from model_name).
            model_parameters (dict): Additional parameters for model configuration.
        """
        self.model_name = model_name.lower()
        self.embedding_model_name = embedding_model_name.lower(
        ) if embedding_model_name else model_name.lower()
        self.api_key = api_key
        self.model_parameters = model_parameters or {}

        # Initialize the language model and embedding model
        self.llm = self._initialize_llm()
        self.embedding_model = self._initialize_embeddings()

    def _initialize_llm(self):
        if self.model_name == "openai":
            return OpenAI(api_key=self.api_key, **self.model_parameters)
        elif self.model_name == "huggingface":
            return HuggingFaceHub(api_key=self.api_key, **self.model_parameters)
        elif self.model_name == "cohere":
            return Cohere(api_key=self.api_key, **self.model_parameters)
        else:
            raise ValueError(f"Unsupported model_name: {self.model_name}")

    def _initialize_embeddings(self):
        if self.embedding_model_name == "openai":
            return OpenAIEmbeddings(api_key=self.api_key)
        elif self.embedding_model_name == "huggingface":
            return HuggingFaceEmbeddings(api_key=self.api_key)
        elif self.embedding_model_name == "cohere":
            return CohereEmbeddings(api_key=self.api_key)
        else:
            raise ValueError(
                f"Unsupported embedding_model_name: {self.embedding_model_name}")

    def generate(self, prompt, max_tokens=100, temperature=0.7):
        """
        Generate a response from the language model.

        Args:
            prompt (str): The input prompt for the LLM.
            max_tokens (int): Maximum number of tokens for the response.
            temperature (float): The temperature parameter for controlling randomness.

        Returns:
            str: Generated text from the LLM.
        """
        response = self.llm(prompt, max_tokens=max_tokens,
                            temperature=temperature)
        return response

    def get_embeddings(self, text):
        """
        Get embeddings for a given text using the specified embedding model.

        Args:
            text (str): The input text for which embeddings are needed.

        Returns:
            List[float]: Embedding vector for the input text.
        """
        return self.embedding_model.embed_query(text)
