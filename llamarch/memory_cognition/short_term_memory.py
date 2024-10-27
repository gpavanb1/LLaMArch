# short_term_memory.py

class ShortTermMemory:
    def __init__(self, vector_db_client):
        """
        Initialize with a vector database client for temporary storage.
        """
        self.vector_db = vector_db_client
        self.temp_store = []  # Temporary list for embeddings

    def store_information(self, vector, info_id):
        """
        Stores embedding in short-term memory and adds it to vector database.
        """
        self.temp_store.append((info_id, vector))
        self.vector_db.add_vectors([vector], [info_id])

    def search_similar(self, query_vector, top_k=5):
        """
        Searches for similar embeddings in short-term memory.
        """
        return self.vector_db.search_vectors(query_vector, top_k)

    def flush_to_long_term(self, long_term_memory):
        """
        Moves temporary embeddings to long-term memory.
        """
        ids, vectors = zip(*self.temp_store) if self.temp_store else ([], [])
        if ids and vectors:
            long_term_memory.store_information(vectors, ids)
            self.temp_store.clear()  # Clear short-term memory
