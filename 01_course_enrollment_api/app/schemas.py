"""Pydantic models - the shape of the data going in and out of the API."""
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CourseCreate(BaseModel):
    """What the client sends to create a course."""
    # strip spaces at both ends before any rule is checked
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=2, max_length=100, examples=["FastAPI Basics"])
    instructor: str = Field(min_length=2, max_length=50, examples=["VK"])

    @field_validator("title")
    @classmethod
    def title_has_letters(cls, value):
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("title must contain at least one letter")
        return " ".join(value.split())          # "FastAPI    Basics" -> "FastAPI Basics"

    @field_validator("instructor")
    @classmethod
    def instructor_is_a_name(cls, value):
        if not re.fullmatch(r"[A-Za-z .]+", value):
            raise ValueError("instructor may contain only letters, spaces and dots")
        return value


class Course(CourseCreate):
    """A saved course. It inherits title and instructor and adds an id."""
    id: int


class Student(BaseModel):
    id: int
    name: str


class EnrollmentCreate(BaseModel):
    """What the client sends to enroll a student in a course."""
    student_id: int = Field(gt=0, examples=[1])
    course_id: int = Field(gt=0, examples=[1])


class Enrollment(EnrollmentCreate):
    """A saved enrollment. It inherits both ids and adds its own id."""
    id: int


class StudentCourse(BaseModel):
    """One row of GET /students/{student_id}/courses."""
    enrollment_id: int
    course: Course
