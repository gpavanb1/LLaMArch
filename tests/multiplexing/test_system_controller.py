import pytest
from system_controller import SystemController


@pytest.fixture
def setup_system():
    large_llm_api_key = "your-openai-api-key"
    system = SystemController(large_llm_api_key)
    return system


def test_handle_query(setup_system):
    query = "Explain the impact of climate change."
    result = setup_system.handle_query(query)
    assert result is not None


def test_unknown_domain_query(setup_system):
    query = "Random query with no matching domain."
    result = setup_system.handle_query(query)
    assert "No specialized model" in result
