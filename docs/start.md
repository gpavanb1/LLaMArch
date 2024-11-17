# Getting Started

Just run 

```
pip install llamarch
```

A basic program is as follows that illustrates the key common components of the framework.

```python
import uuid
from llamarch.common.llm import LLM
from llamarch.common.llm_embedding import LLMEmbedding
from llamarch.common.fine_tuner import FineTuner
from llamarch.common.cache import Cache
from llamarch.common.vector_db import VectorDB
from llamarch.common.graph_db import GraphDB
from llamarch.common.base_agent import GenerativeAIAgent

# Initialize the LLM class
llm = LLM(model_category="huggingface",
          model_name="distilbert/distilgpt2")

# Initialize the LLMEmbedding class
embedding = LLMEmbedding(model_category="huggingface",
                         embedding_model_name="distilbert-base-uncased")

# Initialize the FineTuner class
fine_tuner = FineTuner(llm)

# Initialize the Cache class
cache = Cache()

# Initialize the VectorDB class
vector_db = VectorDB(db_type="qdrant", environment="http://localhost:6333",
                     index_name="default_index", embedding_model=embedding.embedding_model)

# Initialize the GraphDB class
graph_db = GraphDB("bolt://localhost:7687", "neo4j", "testpassword")

# Initialize the GenerativeAIAgent class
agent = GenerativeAIAgent(agent_id="agent1", llm=llm, embedding=embedding)

# Generate a response from the LLM
query = "Hello, how are you?"
agent_reply = agent.llm.generate(query)
print(f"Agent reply: {agent_reply}")

# Fine-tune the LLM
fine_tuner.fine_tune([query])

# Cache the LLM
cache.set(query, agent_reply)

# Query the cache
cached_response = cache.get(query)
print(f"Cached response: {cached_response}")

# Store in VectorDB
info_id = str(uuid.uuid4())
vector_db.add_embeddings(
    info_id, embedding.get_embeddings(query), metadata={"query": query})

# Store in GraphDB
graph_db.write_key_value(info_id, query)

# Query the VectorDB
vector_db_response = vector_db.query_similar(embedding.get_embeddings(query))
print(f"VectorDB response: {vector_db_response}")

# Query the GraphDB
graph_db_response = graph_db.read_by_value(query)
print(f"GraphDB response: {graph_db_response}")
```
