"""StudentService - create, read, update and delete students kept in memory."""
from app.exceptions import EmailTakenError, StudentNotFoundError
from app.schemas import Student, StudentCreate


class StudentService:

    def __init__(self):
        self.students = {}
        self.next_id = 1

    def create(self, data: StudentCreate) -> Student:
        self._check_email_free(data.email)
        student = Student(id=self.next_id, **data.model_dump())
        self.students[student.id] = student
        self.next_id += 1
        return student

    def list_all(self) -> list[Student]:
        return list(self.students.values())

    def get(self, student_id: int) -> Student:
        if student_id not in self.students:
            raise StudentNotFoundError(student_id)
        return self.students[student_id]

    def update(self, student_id: int, data: StudentCreate) -> Student:
        self.get(student_id)                       # 404 if missing
        self._check_email_free(data.email, ignore_id=student_id)
        student = Student(id=student_id, **data.model_dump())
        self.students[student_id] = student
        return student

    def delete(self, student_id: int) -> None:
        self.get(student_id)                       # 404 if missing
        del self.students[student_id]

    def _check_email_free(self, email: str, ignore_id: int = 0) -> None:
        """Two students may not share one email address."""
        for s in self.students.values():
            if s.email == email and s.id != ignore_id:
                raise EmailTakenError(email, s.id)
