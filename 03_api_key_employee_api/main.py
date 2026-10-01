"""API Key Protected Employee API - start it with:  uvicorn main:app --reload"""
from fastapi import FastAPI

from app.exceptions import AppError, app_error_handler
from app.routes import router

app = FastAPI(
    title="Employee API (API key protected)",
    description="GET /employees is public. POST, PUT and DELETE need the X-API-Key header - "
                "click **Authorize** in Swagger UI and paste the key once.",
    version="1.0.0",
)
app.include_router(router)
app.add_exception_handler(AppError, app_error_handler)   # 401, 403 and 404 errors
