import os
import pytest
from fastapi.testclient import TestClient

# Ensure test-friendly settings if needed
os.environ.setdefault("ENABLE_DOCS", "0")
os.environ.setdefault("RATE_LIMIT_PER_MIN", "120")
os.environ.setdefault("ALLOWED_ORIGINS", "*")

from app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
