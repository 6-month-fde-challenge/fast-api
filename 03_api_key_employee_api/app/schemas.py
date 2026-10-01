"""Pydantic models for employee data."""
import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

DEPARTMENTS = ["Engineering", "HR", "Finance", "Sales", "Marketing", "Operations"]


class EmployeeCreate(BaseModel):
    """What the client sends for POST and PUT."""
    # strip spaces at both ends before any rule is checked
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=50, examples=["Priya Nair"])
    email: EmailStr = Field(examples=["priya@example.com"])
    department: str = Field(min_length=2, max_length=30, examples=["Engineering"])
    salary: float = Field(gt=0, le=10_000_000, examples=[85000])

    @field_validator("name")
    @classmethod
    def name_is_letters_only(cls, value):
        if not re.fullmatch(r"[A-Za-z .'-]+", value):
            raise ValueError("name may contain only letters, spaces, dots, hyphens and apostrophes")
        return " ".join(value.split()).title()        # "priya   nair" -> "Priya Nair"

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, value):
        return value.lower()

    @field_validator("department")
    @classmethod
    def department_is_known(cls, value):
        # accept any capitalisation ("engineering"), store the official spelling
        for dept in DEPARTMENTS:
            if value.lower() == dept.lower():
                return dept
        raise ValueError(f"department must be one of: {', '.join(DEPARTMENTS)}")

    @field_validator("salary")
    @classmethod
    def salary_two_decimals(cls, value):
        if round(value, 2) != value:
            raise ValueError("salary may have at most 2 decimal places")
        return value


class Employee(EmployeeCreate):
    """A saved employee. It inherits every field above and adds the id."""
    id: int
