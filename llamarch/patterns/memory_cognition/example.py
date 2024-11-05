# Import memory and Qdrant components
from .short_term_memory import ShortTermMemory
from .long_term_memory import LongTermMemory
from .summarizer import Summarizer  # Summarizer component
from .memory_decay import MemoryDecay  # Memory evaluation and decay component
# Your VectorDB class that supports Qdrant
from llamarch.common.vector_db import VectorDB
from llamarch.common.llm import LLM
from llamarch.common.llm_embedding import LLMEmbedding  # Embedding class

# Initialize the embedding model
embedding = LLMEmbedding(
    model_category="huggingface", embedding_model_name="distilbert-base-uncased"
)

# Initialize the LLM class
llm = LLM(model_category="huggingface",
          model_name="distilbert/distilgpt2")

# Initialize Qdrant clients for Short-Term Memory and Long-Term Memory
stm_client = VectorDB(
    db_type="qdrant", environment="http://localhost:6333", index_name="short_term_memory", embedding_model=embedding.embedding_model
)
ltm_client = VectorDB(
    db_type="qdrant", environment="http://localhost:6333", index_name="long_term_memory", embedding_model=embedding.embedding_model
)

# Initialize memory modules
short_term_memory = ShortTermMemory(stm_client)
long_term_memory = LongTermMemory(ltm_client)
summarizer = Summarizer(llm)  # Summarizer component
memory_decay = MemoryDecay()  # Memory evaluation and decay component


# Example data
query = "Example query text"
query_vector = embedding.get_embeddings(query)

# Step 1: Store query in Short-Term Memory
short_term_memory.store_information(query_vector, query)

# Step 2: Retrieve similar items from Short-Term Memory
similar_items_stm = short_term_memory.fetch_similar(query_vector)
print("Similar items in STM:", [
      getattr(x, "metadata", {}).get("query") for x in similar_items_stm])

# Step 3: Summarize similar items from STM
summary = summarizer.summarize(similar_items_stm)
print("Summary of similar items:", summary)

# Step 4: Evaluate if the summarized information should be stored in Long-Term Memory
if memory_decay.evaluate(summary):
    # Step 5: If evaluation passes, flush summarized information to Long-Term Memory
    short_term_memory.flush_to_long_term(long_term_memory)
    print("Summary flushed to Long-Term Memory.")

# Step 6: Fetch similar items from Long-Term Memory for future queries
long_term_results = long_term_memory.fetch_similar(query_vector)
print("Similar items in LTM:", long_term_results)
