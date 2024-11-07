from llamarch.common.llm import LLM


class Teacher:
    def __init__(self, llm, evaluation_prompt="Evaluate the following response based on relevance, accuracy, and clarity and suggest a better answer:"):
        self.llm = llm
        self.evaluation_prompt = evaluation_prompt

    def evaluate_response(self, student_response):
        """
        Evaluates the student's response by providing feedback or a score.
        """
        # Construct an evaluation prompt
        prompt = f"{self.evaluation_prompt} {student_response}"
        evaluation_text = self.llm.generate(prompt)
        return evaluation_text
