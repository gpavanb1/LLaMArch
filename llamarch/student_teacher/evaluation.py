# evaluation_system.py
from student_llm import StudentLLM
from teacher_llm import TeacherLLM


class EvaluationSystem:
    def __init__(self, student_model_name, teacher_model_name):
        self.student_llm = StudentLLM(student_model_name)
        self.teacher_llm = TeacherLLM(teacher_model_name)

    def evaluate_query(self, query):
        """
        Runs the query through the student LLM, then evaluates the response with the teacher LLM.
        """
        # Step 1: Student LLM generates a response
        student_response = self.student_llm.generate_response(query)
        print(f"Student Response: {student_response}")

        # Step 2: Teacher LLM evaluates the response
        evaluation_feedback = self.teacher_llm.evaluate_response(
            student_response)
        print(f"Teacher Evaluation: {evaluation_feedback}")

        return student_response, evaluation_feedback

    def fine_tune_student(self, feedback_data):
        """
        Fine-tune the student LLM based on feedback. This can be implemented with reinforcement learning or additional supervised training data.
        """
        # Placeholder for fine-tuning the Student LLM
        pass
