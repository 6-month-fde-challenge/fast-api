"""API key check, used as a FastAPI dependency on the protected endpoints."""
import secrets

from fastapi import Security
from fastapi.security import APIKeyHeader

from app.config import API_KEY
from app.exceptions import InvalidApiKeyError, MissingApiKeyError

# Tells FastAPI (and Swagger UI) to look for the key in the X-API-Key header.
# auto_error=False lets us send our own errors instead of FastAPI's default.
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str | None = Security(api_key_header)) -> str:
    # 1. no header at all -> 401 Unauthorized ("who are you?")
    if not api_key:
        raise MissingApiKeyError()
    # 2. header present but wrong -> 403 Forbidden ("I know you tried, but no")
    # compare_digest takes the same time for every wrong key, so an attacker
    # cannot guess the key one character at a time by measuring response times.
    if not secrets.compare_digest(api_key, API_KEY):
        raise InvalidApiKeyError()
    # 3. correct key -> the endpoint runs
    return api_key
