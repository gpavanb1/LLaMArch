# vector_db_client.py

from abc import ABC, abstractmethod


class VectorDBClient(ABC):
    @abstractmethod
    def add_vectors(self, vectors, ids):
        """
        Add vectors to the database.
        """
        pass

    @abstractmethod
    def search_vectors(self, query_vector, top_k=5):
        """
        Search for the top_k most similar vectors.
        """
        pass

# Example subclass for FAISS (extend with Pinecone, Weaviate, etc., as needed)


class FAISSVectorDBClient(VectorDBClient):
    def __init__(self, index):
        self.index = index

    def add_vectors(self, vectors, ids):
        self.index.add_with_ids(vectors, ids)

    def search_vectors(self, query_vector, top_k=5):
        distances, indices = self.index.search(query_vector, top_k)
        return indices, distances  # Return top_k results
