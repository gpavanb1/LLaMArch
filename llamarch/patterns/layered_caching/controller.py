from high_power_llm import HighPowerLLM
from specialized_llm import SpecializedLLM
from cache import Cache
from fine_tuner import FineTuner


class SystemController:
    def __init__(self, large_llm_api_key, smaller_llm):
        self.large_llm = HighPowerLLM(large_llm_api_key)
        self.cache = Cache()
        self.fine_tuner = FineTuner(smaller_llm)
        self.specialized_llm = None  # This will be set after fine-tuning

    def handle_query(self, query):
        # Step 1: Check if the query is cached
        cached_result = self.cache.get(query)
        if cached_result:
            return cached_result

        # Step 2: If not cached, use the large LLM to answer the query
        result = self.large_llm.query(query)

        # Cache the result for future use
        self.cache.set(query, result)

        # Step 3: Fine-tune the smaller model based on cached results
        if not self.specialized_llm:
            data = list(self.cache.store.values())  # Use all cached results
            fine_tuned_model = self.fine_tuner.fine_tune(data)
            self.specialized_llm = SpecializedLLM(fine_tuned_model)

        return result

    def handle_future_query(self, query):
        # Use the smaller fine-tuned model for future queries
        return self.specialized_llm.query(query)
