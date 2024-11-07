from llamarch.common.llm import LLM
from llamarch.common.fine_tuner import FineTuner


class Student:
    def __init__(self, llm):
        self.llm = llm
        self.fine_tuner = FineTuner(llm)

    def generate_response(self, query):
        """
        Generates a response for the given query using the student LLM.
        """
        return self.llm.generate(query)

    def fine_tune(self, data):
        """
        Fine-tunes the student LLM on the given data.
        """
        self.llm = self.fine_tuner.fine_tune(data)
