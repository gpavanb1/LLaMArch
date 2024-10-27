# main.py

from short_term_memory import ShortTermMemory
from long_term_memory import LongTermMemory
# Add Pinecone, Weaviate, etc.
from vector_db_client import FAISSVectorDBClient, VectorDBClient

# Initialize vector databases (example for FAISS, replace with actual initialization)
from faiss import IndexFlatL2

# Initialize FAISS with 512 dimensions
faiss_index = IndexFlatL2(dimension=512)
faiss_client = FAISSVectorDBClient(faiss_index)

# For Pinecone, you'd use its own client (assuming pinecone_client is already set up)
# pinecone_client = PineconeVectorDBClient(pinecone_index)

# Instantiate memory modules
short_term_memory = ShortTermMemory(faiss_client)
# Could be separate clients for ST and LT
long_term_memory = LongTermMemory(faiss_client)

# Example data
query = "Example query"
query_vector = [0.1] * 512  # Replace with actual vector representation

# Store and search in Short-Term Memory
short_term_memory.store_information(query_vector, "temp_id_1")
similar_items = short_term_memory.search_similar(query_vector)

# Transfer to Long-Term Memory
short_term_memory.flush_to_long_term(long_term_memory)

# Fetch from Long-Term Memory
long_term_results = long_term_memory.fetch_similar(query_vector)
