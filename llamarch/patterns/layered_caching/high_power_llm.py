from langchain.llms import OpenAI


class HighPowerLLM:
    def __init__(self, api_key):
        self.llm = OpenAI(api_key=api_key)

    def query(self, text):
        # Query the LLM
        return self.llm(text)
