"""The five CRUD endpoints for /students."""
from fastapi import APIRouter

from app.schemas import Student, StudentCreate
from app.service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])
service = StudentService()

# Error responses listed here also show up in Swagger UI next to each endpoint.
NOT_FOUND = {404: {"description": "No student with this id"}}
EMAIL_TAKEN = {409: {"description": "Another student already uses this email"}}


@router.post("", response_model=Student, status_code=201, responses=EMAIL_TAKEN)
def create_student(student: StudentCreate):
    return service.create(student)


@router.get("", response_model=list[Student])
def get_students():
    return service.list_all()


@router.get("/{student_id}", response_model=Student, responses=NOT_FOUND)
def get_student(student_id: int):
    return service.get(student_id)


@router.put("/{student_id}", response_model=Student, responses={**NOT_FOUND, **EMAIL_TAKEN})
def update_student(student_id: int, student: StudentCreate):
    return service.update(student_id, student)


@router.delete("/{student_id}", status_code=204, responses=NOT_FOUND)
def delete_student(student_id: int):
    service.delete(student_id)
