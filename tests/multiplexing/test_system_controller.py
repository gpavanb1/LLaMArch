import pytest
from llamarch.patterns.layered_caching import LayeredCaching as SystemController


@pytest.fixture
def setup_system():
    # LayeredCaching needs two LLMs
    from llamarch.common.llm import LLM
    large_llm = LLM(model_category="huggingface", model_name="distilbert/distilgpt2")
    small_llm = LLM(model_category="huggingface", model_name="distilbert/distilgpt2")
    system = SystemController(large_llm, small_llm)
    
    # Clear the cache before tests
    system.cache.flush()
    
    yield system
    
    # Clear the cache after tests
    system.cache.flush()


def test_handle_query(setup_system):
    query = "Explain the impact of climate change."
    result = setup_system.handle_query(query)
    assert result is not None


def test_unknown_domain_query(setup_system):
    query = "Random query with no matching domain."
    result = setup_system.handle_query(query)
    # The current handle_query always returns a result or fails
    assert result is not None
