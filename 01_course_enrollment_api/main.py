"""Course Enrollment API - start it with:  uvicorn main:app --reload"""
from fastapi import FastAPI

from app.exceptions import AppError, app_error_handler
from app.routes import router

app = FastAPI(
    title="Course Enrollment API",
    description="Create courses and enroll students in them. "
                "Ready-made students: 1 Aarav, 2 Diya, 3 Rahul.",
    version="1.0.0",
)
app.include_router(router)
app.add_exception_handler(AppError, app_error_handler)   # NotFoundError, AlreadyEnrolledError, ...
