from llamarch.common.llm import LLM
from llamarch.common.graph_db import GraphDB


class KnowledgeLLM:
    def __init__(self, knowledge_graph: GraphDB, llm: LLM):
        self.knowledge_graph = knowledge_graph
        self.llm = llm

    def query_knowledge_graph(self, query):
        # Query the knowledge graph
        return self.knowledge_graph.read_data(query)

    def update_knowledge_graph(self, query, parameters=None):
        # Update the knowledge graph
        self.knowledge_graph.write_data(query, parameters)

    def generate_ontology(self, text):
        # Use the LLM to generate ontology
        prompt = f"Generate an ontology from the following text: {text}"
        ontology = self.llm.generate(prompt)
        # Insert the generated ontology into the knowledge graph
        self.update_knowledge_graph(
            "CREATE (n:Ontology {data: $ontology})", {"ontology": ontology})
        return ontology

    def respond_to_query(self, query):
        # Query the LLM using existing knowledge and graph data
        graph_result = self.query_knowledge_graph(query)
        prompt = f"Given this knowledge: {graph_result}, answer the following query: {query}"
        print(prompt)
        return self.llm(prompt)
