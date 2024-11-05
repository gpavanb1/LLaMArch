# short_term_memory.py
import uuid
from .long_term_memory import LongTermMemory
from typing import List, Tuple
from llamarch.common.vector_db import VectorDB


class ShortTermMemory:
    def __init__(self, vector_db_client: VectorDB):
        """
        Initialize with a vector database client for temporary storage.

        Args:
            vector_db_client (VectorDB): An instance of the VectorDB class for short-term storage.
        """
        self.vector_db = vector_db_client
        # Temporary list for embeddings
        self.temp_store: List[Tuple[str, List[float]]] = []

    def store_information(self, vector: List[float], query: str):
        """
        Stores embedding in short-term memory and adds it to the vector database.

        Args:
            vector (List[float]): The embedding vector to store.
            query (str): The original query or context associated with the embedding.
        """
        info_id = str(uuid.uuid4())
        # Store ID, vector, and query
        self.temp_store.append((info_id, vector, query))
        self.vector_db.add_embeddings(info_id, vector, metadata={
                                      'query': query})

    def fetch_similar(self, query_vector: List[float], top_k: int = 5) -> List[dict]:
        """
        Searches for similar embeddings in short-term memory.

        Args:
            query_vector (List[float]): The embedding vector to search for similar vectors.
            top_k (int): Number of similar vectors to retrieve.

        Returns:
            List[dict]: List of similar embedding results.
        """
        return self.vector_db.query_similar(query_vector, top_k)

    def flush_to_long_term(self, long_term_memory: LongTermMemory):
        """
        Moves temporary embeddings to long-term memory.

        Args:
            long_term_memory (LongTermMemory): An instance of LongTermMemory to store embeddings.
        """
        if self.temp_store:
            ids, vectors = zip(*self.temp_store)
            long_term_memory.store_information(vectors, ids)
            self.temp_store.clear()  # Clear short-term memory
