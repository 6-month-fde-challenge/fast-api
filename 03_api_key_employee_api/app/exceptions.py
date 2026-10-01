"""Custom exceptions. The app raises these; one handler turns them into JSON."""
from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for every error this API raises on purpose."""
    status_code = 400
    headers = None          # extra response headers, if a subclass needs them

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class MissingApiKeyError(AppError):
    """No X-API-Key header -> 401. Tells the client how to authenticate."""
    status_code = 401
    headers = {"WWW-Authenticate": "APIKey"}

    def __init__(self):
        super().__init__("Missing API key. Send it in the X-API-Key header.")


class InvalidApiKeyError(AppError):
    """X-API-Key header present but wrong -> 403."""
    status_code = 403

    def __init__(self):
        super().__init__("Invalid API key.")


class EmployeeNotFoundError(AppError):
    status_code = 404

    def __init__(self, employee_id: int):
        super().__init__(f"Employee {employee_id} not found")


def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    # every subclass brings its own status_code (and headers), so one handler serves them all
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message}, headers=exc.headers)
