from langchain_community.vectorstores import Pinecone, Weaviate, Chroma
from langchain_qdrant import QdrantVectorStore
from typing import List, Union


class VectorDB:
    def __init__(self, db_type="pinecone", api_key=None, environment=None, index_name="default_index", embedding_model=None):
        """
        Initialize the vector database client based on the specified type.

        Args:
            db_type (str): Type of vector database (e.g., 'pinecone', 'weaviate', 'qdrant', 'chroma').
            api_key (str): API key for the vector database (if required).
            environment (str): Environment or URL for the vector database (if required).
            index_name (str): Name of the index or collection in the vector database.
            embeddings: Required for Qdrant, the embedding model used
        """
        self.db_type = db_type.lower()
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.embedding_model = embedding_model
        self.client = self._initialize_client()

    def _initialize_client(self):
        # Initialize based on database type
        if self.db_type == "pinecone":
            import pinecone
            pinecone.init(api_key=self.api_key, environment=self.environment)
            return Pinecone(index_name=self.index_name)

        elif self.db_type == "weaviate":
            import weaviate
            client = weaviate.Client(url=self.environment)
            return Weaviate(client=client, index_name=self.index_name)

        elif self.db_type == "qdrant":
            from qdrant_client import QdrantClient
            client = QdrantClient(api_key=self.api_key, url=self.environment)
            return QdrantVectorStore(client=client, collection_name=self.index_name, embedding=self.embedding_model)

        elif self.db_type == "chroma":
            return Chroma(collection_name=self.index_name)

        else:
            raise ValueError(f"Unsupported db_type: {self.db_type}")

    def add_embeddings(self, vector_id: str, embedding: List[float], metadata: dict = None):
        """
        Add an embedding to the vector database.

        Args:
            vector_id (str): Unique identifier for the vector.
            embedding (List[float]): The embedding vector.
            metadata (dict): Additional metadata to store with the vector.
        """
        self.client.add_texts(
            texts=[str(embedding)],
            metadatas=[metadata],
            ids=[vector_id]
        )

    def query_similar(self, embedding: List[float], top_k: int = 5) -> List[Union[dict, str]]:
        """
        Query for similar embeddings in the vector database.

        Args:
            embedding (List[float]): The embedding vector to search.
            top_k (int): Number of similar vectors to retrieve.

        Returns:
            List[Union[dict, str]]: List of results from the vector database.
        """
        results = self.client.similarity_search_by_vector(embedding, k=top_k)
        return results
