# long_term_memory.py

class LongTermMemory:
    def __init__(self, vector_db_client):
        """
        Initialize with a vector database client for long-term storage.
        """
        self.vector_db = vector_db_client

    def store_information(self, vectors, ids):
        """
        Stores embeddings in long-term memory using the vector database.
        """
        self.vector_db.add_vectors(vectors, ids)

    def fetch_similar(self, query_vector, top_k=5):
        """
        Fetches similar embeddings from long-term memory.
        """
        return self.vector_db.search_vectors(query_vector, top_k)
