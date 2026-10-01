"""Mini E-Commerce Order API - start it with:  uvicorn main:app --reload"""
from fastapi import FastAPI

from app.exceptions import AppError, app_error_handler
from app.routes import router

app = FastAPI(
    title="Mini E-Commerce Order API",
    description="Add products, place orders and move them through "
                "PLACED -> PROCESSING -> SHIPPED -> DELIVERED. "
                "The server calculates every total.",
    version="1.0.0",
)
app.include_router(router)
app.add_exception_handler(AppError, app_error_handler)   # 404 and 400 business errors
