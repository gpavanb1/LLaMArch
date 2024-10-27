from langchain.llms import OpenAI


class GeneralPurposeLLM:
    def __init__(self, api_key):
        self.llm = OpenAI(api_key=api_key)

    def process_query(self, query):
        # General purpose LLM processes the query and returns context
        return self.llm(query)
