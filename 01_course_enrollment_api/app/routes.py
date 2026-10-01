"""The five endpoints. Each one only calls the service and returns the result."""
from fastapi import APIRouter

from app.schemas import Course, CourseCreate, Enrollment, EnrollmentCreate, StudentCourse
from app.service import EnrollmentService

router = APIRouter()
service = EnrollmentService()

# Error responses listed here also show up in Swagger UI next to each endpoint.
NOT_FOUND = {404: {"description": "Student, course or enrollment not found"}}
DUPLICATE = {409: {"description": "Student is already enrolled in this course"}}


@router.post("/courses", response_model=Course, status_code=201, tags=["Courses"])
def create_course(course: CourseCreate):
    return service.add_course(course)


@router.get("/courses", response_model=list[Course], tags=["Courses"])
def get_courses():
    return service.list_courses()


@router.post("/enroll", response_model=Enrollment, status_code=201, tags=["Enrollments"],
             responses={**NOT_FOUND, **DUPLICATE})
def enroll_student(enrollment: EnrollmentCreate):
    return service.enroll(enrollment)


@router.get("/students/{student_id}/courses", response_model=list[StudentCourse], tags=["Enrollments"],
            responses=NOT_FOUND)
def get_student_courses(student_id: int):
    return service.courses_of_student(student_id)


@router.delete("/enroll/{enrollment_id}", status_code=204, tags=["Enrollments"], responses=NOT_FOUND)
def delete_enrollment(enrollment_id: int):
    service.unenroll(enrollment_id)
