"""Settings. The API key is read from the environment, never hard-coded as a real secret.

Put your own key in a .env file (copy .env.example). .env is git-ignored,
so the real key never reaches GitHub. If no key is set, the public demo key
from the task statement is used so the project still runs from a fresh clone.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# reads 03_api_key_employee_api/.env, if it exists
load_dotenv(Path(__file__).parent.parent / ".env")

DEMO_API_KEY = "super30-secret-key"
API_KEY = os.getenv("API_KEY", DEMO_API_KEY)
