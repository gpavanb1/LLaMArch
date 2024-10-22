import pytest
# Assuming the class is in knowledge_graph.py
from knowledge_graph import KnowledgeGraph


@pytest.fixture(scope="module")
def kg():
    # Connect to the local Neo4j database
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"  # Replace with your Neo4j password
    kg_instance = KnowledgeGraph(uri, user, password)
    yield kg_instance
    kg_instance.close()  # Ensure the connection is closed after tests


def test_write_data(kg):
    query = "CREATE (n:Person {name: $name})"
    parameters = {"name": "Alice"}
    kg.write_data(query, parameters)

    # Verify the data was written
    query_check = "MATCH (n:Person {name: $name}) RETURN n"
    result = kg.read_data(query_check, parameters)
    assert len(result) > 0  # Ensure that the node was created


def test_read_data(kg):
    query = "MATCH (n:Person {name: $name}) RETURN n"
    parameters = {"name": "Alice"}
    result = kg.read_data(query, parameters)

    assert len(result) > 0  # Ensure the data is read correctly
    assert result[0]["name"] == "Alice"  # Check the returned data


def test_execute_query(kg):
    query = "MATCH (n:Person) RETURN count(n) AS count"
    result = kg.read_data(query)

    assert len(result) > 0  # Ensure the query executed successfully
    assert result[0]["count"] >= 1  # Ensure at least one person exists


def test_close(kg):
    # The close method will be tested indirectly through the fixture teardown.
    pass  # No action needed, as closing is handled by the fixture
