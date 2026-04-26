import os
import pytest

from app import create_app


@pytest.fixture
def app():
    test_database_url = os.getenv("TEST_DATABASE_URL")

    if not test_database_url:
        pytest.skip("TEST_DATABASE_URL is not set. Skipping PostgreSQL integration tests.")

    app = create_app({
        "TESTING": True,
        "DATABASE_URL": test_database_url,
        "CORS_ORIGINS": ["http://localhost:3000"],
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()