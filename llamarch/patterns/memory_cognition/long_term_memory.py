# long_term_memory.py
from typing import List


class LongTermMemory:
    def __init__(self, vector_db_client: 'VectorDB'):
        """
        Initialize with a vector database client for long-term storage.

        Args:
            vector_db_client (VectorDB): An instance of the VectorDB class for long-term storage.
        """
        self.vector_db = vector_db_client

    def store_information(self, vectors: List[List[float]], ids: List[str]):
        """
        Stores embeddings in long-term memory using the vector database.

        Args:
            vectors (List[List[float]]): List of embeddings to store.
            ids (List[str]): Corresponding unique identifiers for each embedding.
        """
        for vector_id, embedding in zip(ids, vectors):
            self.vector_db.add_embeddings(vector_id, embedding)

    def fetch_similar(self, query_vector: List[float], top_k: int = 5) -> List[dict]:
        """
        Fetches similar embeddings from long-term memory.

        Args:
            query_vector (List[float]): The embedding vector to search for similar vectors.
            top_k (int): Number of similar vectors to retrieve.

        Returns:
            List[dict]: List of similar embedding results.
        """
        return self.vector_db.query_similar(query_vector, top_k)
