import os
import pytest
from fastapi.testclient import TestClient

# Ensure test ENV
os.environ.setdefault("ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("PROMETHEUS_ENABLE", "0")  # keep metrics quiet in tests

from apps.api.app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
