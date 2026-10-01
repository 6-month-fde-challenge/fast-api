"""Pydantic models - every request body is checked against these before our code runs."""
import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StudentCreate(BaseModel):
    """What the client sends for POST and PUT."""
    # strip spaces at both ends before any rule is checked
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=50, examples=["Aarav Sharma"])
    email: EmailStr = Field(examples=["aarav@example.com"])
    age: int = Field(ge=5, le=100, examples=[21])
    course: str = Field(min_length=2, max_length=50, examples=["FastAPI"])

    @field_validator("name")
    @classmethod
    def name_is_letters_only(cls, value):
        if not re.fullmatch(r"[A-Za-z .'-]+", value):
            raise ValueError("name may contain only letters, spaces, dots, hyphens and apostrophes")
        return " ".join(value.split()).title()        # "aarav   sharma" -> "Aarav Sharma"

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, value):
        # so Aarav@Example.com and aarav@example.com count as the same email
        return value.lower()

    @field_validator("course")
    @classmethod
    def course_has_letters(cls, value):
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("course must contain at least one letter")
        return value


class Student(StudentCreate):
    """A saved student. It inherits every field above and adds the id."""
    id: int
