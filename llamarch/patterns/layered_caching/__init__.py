from llamarch.common.llm import LLM
from llamarch.common.cache import Cache
from .fine_tuner import FineTuner


class LayeredCaching:
    def __init__(self, large_llm, small_llm):
        self.large_llm = large_llm
        self.fine_tuner = FineTuner(small_llm)
        self.cache = Cache()
        self.specialized_llm = None  # This will be set after fine-tuning

    def handle_query(self, query):
        # Step 1: Check if the query is cached
        cached_result = self.cache.get(query)
        if cached_result:
            return cached_result

        # Step 2: If not cached, use the large LLM to answer the query
        result = self.large_llm.generate(query)

        # Cache the result for future use
        self.cache.set(query, result)

        # Step 3: Fine-tune the smaller model based on cached results
        print(self.specialized_llm)
        if not self.specialized_llm:
            data = self.cache.get_all_values()  # Use all cached results
            print(data)
            self.specialized_llm = self.fine_tuner.fine_tune(data)
            print('Fine-tuned model loaded')
        return result

    def handle_future_query(self, query):
        # Use the smaller fine-tuned model for future queries
        return self.specialized_llm.generate(query)
