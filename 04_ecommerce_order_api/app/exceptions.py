"""Custom exceptions. The services raise these; one handler turns them into JSON."""
from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for every error this API raises on purpose."""
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    """A product or order id does not exist."""
    status_code = 404


class OutOfStockError(AppError):
    """The order asks for more than the catalogue has."""
    status_code = 400

    def __init__(self, product_name: str, in_stock: int, asked: int):
        super().__init__(f"Only {in_stock} '{product_name}' left in stock, you asked for {asked}")


class InvalidStatusChangeError(AppError):
    """The status may only move one step forward."""
    status_code = 400


def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    # every subclass brings its own status_code, so one handler serves them all
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
