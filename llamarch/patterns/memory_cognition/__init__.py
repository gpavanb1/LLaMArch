import logging


class MemoryCognition:
    def __init__(self, llm, embedding, short_term_memory, long_term_memory, summarizer, memory_decay):
        self.llm = llm
        self.embedding = embedding
        self.short_term_memory = short_term_memory
        self.long_term_memory = long_term_memory
        self.summarizer = summarizer
        self.memory_decay = memory_decay
        self.logger = logging.getLogger(__name__)
        self.logger.info("MemoryCognition initialized.")

    def store_information(self, query, query_vector):
        self.short_term_memory.store_information(query_vector, query)
        self.logger.info(f"Information stored in Short-Term Memory: {query}")

    def fetch_similar(self, query_vector):
        similar_items_stm = self.short_term_memory.fetch_similar(query_vector)
        self.logger.info(
            f"Similar items in Short-Term Memory: {[getattr(x, 'metadata', {}).get('query') for x in similar_items_stm]}")
        return similar_items_stm

    def summarize(self, similar_items_stm):
        summary = self.summarizer.summarize(similar_items_stm)
        self.logger.info(f"Summary of similar items: {summary}")
        return summary

    def evaluate(self, summary):
        evaluation = self.memory_decay.evaluate(summary)
        self.logger.info(f"Evaluation: {evaluation}")
        return evaluation

    def flush_to_long_term(self, long_term_memory):
        self.short_term_memory.flush_to_long_term(long_term_memory)
        self.logger.info("Summary flushed to Long-Term Memory.")

    def fetch_similar_from_long_term(self, query_vector):
        long_term_results = self.long_term_memory.fetch_similar(query_vector)
        self.logger.info(
            f"Similar items in Long-Term Memory: {long_term_results}")
