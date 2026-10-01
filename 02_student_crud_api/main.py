"""Student CRUD API - start it with:  uvicorn main:app --reload"""
from fastapi import FastAPI

from app.exceptions import AppError, app_error_handler
from app.routes import router

app = FastAPI(
    title="Student CRUD API",
    description="Create, read, update and delete students. Data is validated with Pydantic.",
    version="1.0.0",
)
app.include_router(router)
app.add_exception_handler(AppError, app_error_handler)   # StudentNotFoundError, EmailTakenError
