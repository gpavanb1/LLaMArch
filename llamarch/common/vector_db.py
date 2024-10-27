from typing import List
# Replace with actual vector DB library (e.g., Pinecone, Weaviate)
import some_vector_db_library


class VectorDB:
    def __init__(self, api_key, environment):
        self.client = some_vector_db_library.Client(
            api_key=api_key, environment=environment)

    def add_embeddings(self, vector_id: str, embedding: List[float], metadata: dict = None):
        self.client.upsert(vector_id=vector_id,
                           vector=embedding, metadata=metadata)

    def query_similar(self, embedding: List[float], top_k: int = 5):
        return self.client.query(vector=embedding, top_k=top_k)
