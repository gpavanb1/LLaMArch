# main.py
from evaluation_system import EvaluationSystem

# Specify the names or paths of the pre-trained models
student_model_name = "path/to/fine-tuned-student-llm"
teacher_model_name = "path/to/fine-tuned-teacher-llm"

# Initialize the evaluation system
evaluation_system = EvaluationSystem(student_model_name, teacher_model_name)

# Define a query for testing
query = "Explain the importance of data privacy in the digital age."

# Run evaluation
student_response, evaluation_feedback = evaluation_system.evaluate_query(query)

# Use the feedback to further fine-tune or adjust the Student LLM if needed
evaluation_system.fine_tune_student(evaluation_feedback)
