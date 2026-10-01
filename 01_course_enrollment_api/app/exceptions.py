"""Custom exceptions. The service raises these; one handler turns them into JSON."""
from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for every error this API raises on purpose."""
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    """A student, course or enrollment id does not exist."""
    status_code = 404


class AlreadyEnrolledError(AppError):
    """The student is already enrolled in this course."""
    status_code = 409


def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    # every subclass brings its own status_code, so one handler serves them all
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
