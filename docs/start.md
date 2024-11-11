# Getting Started

Just run 

```
pip install llamarch
```

A basic program is as follows:

```python
from llamarch.common.llm import LLM
from llamarch.common.llm_embedding import LLMEmbedding
from llamarch.common.fine_tuner import FineTuner
from llamarch.common.cache import Cache
from llamarch.common.vector_db import VectorDB
from llamarch.common.graph_db import GraphDB
from llamarch.common.base_agent import GenerativeAIAgent

# Initialize the LLM class
llm = LLM(model_category="huggingface",
          model_name="gpt2",
          api_key="YOUR_API_KEY")

# Initialize the LLMEmbedding class
embedding = LLMEmbedding(model_category="huggingface", embedding_model_name="distilbert-base-uncased")

# Initialize the FineTuner class
fine_tuner = FineTuner(llm)

# Initialize the Cache class
cache = Cache(llm, embedding)

# Initialize the VectorDB class
vector_db = VectorDB(db_type="qdrant", environment="http://localhost:6333", index_name="default_index", embedding_model=embedding.embedding_model)

# Initialize the GraphDB class
graph_db = GraphDB(db_type="neo4j", environment="http://localhost:7474", index_name="default_index")

# Initialize the GenerativeAIAgent class
agent = GenerativeAIAgent(agent_id="agent1", llm=llm, embedding=embedding)

# Generate a response from the LLM
response = agent.generate_response("Hello, how are you?")
print(response.response)

# Fine-tune the LLM
fine_tuner.fine_tune(["Hello, how are you?"])

# Cache the LLM
cache.cache(response.response)

# Query the cache
cached_response = cache.query("Hello, how are you?")
print(cached_response)

# Query the VectorDB
vector_db_response = vector_db.query_similar(embedding.get_embeddings("Hello, how are you?"))
print(vector_db_response)

# Query the GraphDB
graph_db_response = graph_db.query_similar(embedding.get_embeddings("Hello, how are you?"))
print(graph_db_response)
```
