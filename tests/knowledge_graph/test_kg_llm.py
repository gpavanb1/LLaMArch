import os
import pytest
from langchain.llms import OpenAI
# Assuming the class is in knowledge_graph.py
from patterns.knowledge_graph.knowledge_graph import KnowledgeGraph
# Assuming the class is in knowledge_llm.py
from patterns.knowledge_graph.knowledge_llm import KnowledgeLLM


@pytest.fixture(scope="module")
def kg():
    # Connect to the local Neo4j database
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"  # Replace with your Neo4j password
    kg_instance = KnowledgeGraph(uri, user, password)
    yield kg_instance
    kg_instance.close()  # Ensure the connection is closed after tests


@pytest.fixture(scope="module")
def llm():
    # Set up the LLM instance with the OpenAI API key
    # Make sure to set this environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    llm_instance = OpenAI(api_key=api_key)
    yield llm_instance


@pytest.fixture(scope="module")
def knowledge_llm(kg, llm):
    # Create an instance of KnowledgeLLM
    kl_instance = KnowledgeLLM(kg, llm)
    yield kl_instance


def clear_test_data(knowledge_llm):
    # Clean up the Knowledge Graph by deleting any existing test nodes
    queries = [
        "MATCH (n:Ontology) DETACH DELETE n",
        "MATCH (n:Person) DETACH DELETE n",
        "MATCH (n:Architecture) DETACH DELETE n"
    ]
    for query in queries:
        knowledge_llm.update_knowledge_graph(query)


def test_query_knowledge_graph(knowledge_llm):
    clear_test_data(knowledge_llm)  # Ensure clean state before the test

    query = "MATCH (n:Ontology) RETURN n"
    result = knowledge_llm.query_knowledge_graph(query)
    assert result is None  # Assuming no ontology exists yet


def test_generate_ontology(knowledge_llm):
    clear_test_data(knowledge_llm)  # Ensure clean state before the test

    text = "Sample text for ontology generation."
    ontology = knowledge_llm.generate_ontology(text)

    # Verify that the ontology was generated and stored in the knowledge graph
    query_check = "MATCH (n:Ontology {data: $data}) RETURN n"
    parameters = {"data": ontology}
    result = knowledge_llm.query_knowledge_graph(query_check)

    assert len(result) > 0  # Ensure the ontology was created
    assert result[0]["data"] == ontology  # Check the stored ontology data


def test_update_knowledge_graph(knowledge_llm):
    clear_test_data(knowledge_llm)  # Ensure clean state before the test

    # Add a sample node to the knowledge graph
    query = "CREATE (n:Person {name: $name})"
    parameters = {"name": "Alice"}
    knowledge_llm.update_knowledge_graph(query, parameters)

    # Verify the data was written
    query_check = "MATCH (n:Person {name: $name}) RETURN n"
    result = knowledge_llm.query_knowledge_graph(query_check)

    assert len(result) > 0  # Ensure that the node was created
    assert result[0]["name"] == "Alice"  # Check the returned data


def test_respond_to_query(knowledge_llm):
    clear_test_data(knowledge_llm)  # Ensure clean state before the test

    # First, ensure there is some data to respond to
    knowledge_llm.update_knowledge_graph(
        "CREATE (n:Architecture {description: 'A structure.'})",
        {"description": "A structure."}
    )

    # Mocking response from LLM
    query = "What is the architecture?"
    response = knowledge_llm.respond_to_query(query)

    # Here you should check if the response contains the expected information.
    assert isinstance(response, str)  # Ensure that the response is a string


def test_close(knowledge_llm):
    # The close method will be tested indirectly through the fixture teardown.
    pass  # No action needed, as closing is handled by the fixture
