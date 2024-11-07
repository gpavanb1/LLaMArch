from .student import Student
from .teacher import Teacher


MAX_LENGTH = 300


class StudentTeacher:
    def __init__(self, student_llm, teacher_llm):
        self.student = Student(student_llm)
        self.teacher = Teacher(teacher_llm)

    def generate_response(self, query):
        """
        Generates a response from the student and teacher LLMs.
        """
        student_response = self.student.generate_response(query)
        teacher_response = self.teacher.evaluate_response(
            student_response[:MAX_LENGTH])
        return student_response, teacher_response

    def train_student(self, data):
        self.student.fine_tune(data)
