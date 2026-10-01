"""EnrollmentService - holds the data and applies the business rules."""
from app.exceptions import AlreadyEnrolledError, NotFoundError
from app.schemas import Course, CourseCreate, Enrollment, EnrollmentCreate, Student, StudentCourse


class EnrollmentService:
    """Keeps courses, students and enrollments in memory (plain dictionaries)."""

    def __init__(self):
        self.courses = {}
        self.enrollments = {}
        self.next_course_id = 1
        self.next_enrollment_id = 1
        # The task has no endpoint to create students, so a few are ready-made.
        self.students = {
            1: Student(id=1, name="Aarav"),
            2: Student(id=2, name="Diya"),
            3: Student(id=3, name="Rahul"),
        }

    # ---------- courses ----------
    def add_course(self, data: CourseCreate) -> Course:
        course = Course(id=self.next_course_id, **data.model_dump())
        self.courses[course.id] = course
        self.next_course_id += 1
        return course

    def list_courses(self) -> list[Course]:
        return list(self.courses.values())

    # ---------- enrollments ----------
    def enroll(self, data: EnrollmentCreate) -> Enrollment:
        self._get_student(data.student_id)
        self._get_course(data.course_id)

        for e in self.enrollments.values():
            if e.student_id == data.student_id and e.course_id == data.course_id:
                raise AlreadyEnrolledError(
                    f"Student {data.student_id} is already enrolled in course {data.course_id}")

        enrollment = Enrollment(id=self.next_enrollment_id, **data.model_dump())
        self.enrollments[enrollment.id] = enrollment
        self.next_enrollment_id += 1
        return enrollment

    def courses_of_student(self, student_id: int) -> list[StudentCourse]:
        self._get_student(student_id)
        result = []
        for e in self.enrollments.values():
            if e.student_id == student_id:
                result.append(StudentCourse(enrollment_id=e.id, course=self.courses[e.course_id]))
        return result

    def unenroll(self, enrollment_id: int) -> None:
        if enrollment_id not in self.enrollments:
            raise NotFoundError(f"Enrollment {enrollment_id} not found")
        del self.enrollments[enrollment_id]

    # ---------- helpers ----------
    def _get_student(self, student_id: int) -> Student:
        if student_id not in self.students:
            raise NotFoundError(f"Student {student_id} not found")
        return self.students[student_id]

    def _get_course(self, course_id: int) -> Course:
        if course_id not in self.courses:
            raise NotFoundError(f"Course {course_id} not found")
        return self.courses[course_id]
