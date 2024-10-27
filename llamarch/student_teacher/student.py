# student_llm.py
from transformers import AutoModelForCausalLM, AutoTokenizer


class StudentLLM:
    def __init__(self, model_name):
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_response(self, query):
        """
        Generates a response for the given query using the student LLM.
        """
        inputs = self.tokenizer(query, return_tensors="pt")
        outputs = self.model.generate(
            **inputs, max_length=100, temperature=0.7)
        response_text = self.tokenizer.decode(
            outputs[0], skip_special_tokens=True)
        return response_text
