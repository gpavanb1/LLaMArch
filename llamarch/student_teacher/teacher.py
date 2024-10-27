# teacher_llm.py
from transformers import AutoModelForCausalLM, AutoTokenizer


class TeacherLLM:
    def __init__(self, model_name, evaluation_prompt="Evaluate the following response based on relevance, accuracy, and clarity:"):
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.evaluation_prompt = evaluation_prompt

    def evaluate_response(self, student_response):
        """
        Evaluates the student's response by providing feedback or a score.
        """
        # Construct an evaluation prompt
        prompt = f"{self.evaluation_prompt} {student_response}"
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=50, temperature=0.7)
        evaluation_text = self.tokenizer.decode(
            outputs[0], skip_special_tokens=True)
        return evaluation_text
