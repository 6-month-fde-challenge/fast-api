"""Custom exceptions. The service raises these; one handler turns them into JSON."""
from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for every error this API raises on purpose."""
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class StudentNotFoundError(AppError):
    status_code = 404

    def __init__(self, student_id: int):
        super().__init__(f"Student {student_id} not found")


class EmailTakenError(AppError):
    status_code = 409

    def __init__(self, email: str, owner_id: int):
        super().__init__(f"Email {email} is already used by student {owner_id}")


def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    # every subclass brings its own status_code, so one handler serves them all
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
