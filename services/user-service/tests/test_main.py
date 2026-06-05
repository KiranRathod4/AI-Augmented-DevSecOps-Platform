# services/user-service/tests/test_main.py

import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["TESTING"] = "true"

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402

# ── In-memory SQLite for tests ─────────────────────────────────────────────────
# StaticPool: same connection shared across the test (needed for in-memory SQLite)
# connect_args check_same_thread=False: SQLite default is single-thread, override for tests
SQLITE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Replace the real PostgreSQL session with an in-memory SQLite session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Pytest fixtures ────────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def client():
    """
    Module-scoped fixture: tables created once, shared across all tests in file.
    FastAPI dependency override replaces get_db with our test version.
    """
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clean_db():
    """
    Function-scoped (autouse): wipes and recreates tables before each test.
    This gives each test a clean slate without needing a fresh engine.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# ── Tests ──────────────────────────────────────────────────────────────────────
class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["service"] == "user-service"


class TestCreateUser:
    def test_create_user_returns_201(self, client):
        payload = {"name": "Priya Sharma", "email": "priya@test.io"}
        r = client.post("/users", json=payload)
        assert r.status_code == 201

    def test_create_user_response_has_correct_fields(self, client):
        r = client.post("/users", json={"name": "Arjun Dev", "email": "arjun@test.io"})
        data = r.json()
        assert data["name"] == "Arjun Dev"
        assert data["email"] == "arjun@test.io"
        assert "id" in data
        assert "created_at" in data

    def test_create_user_assigns_auto_increment_id(self, client):
        r1 = client.post("/users", json={"name": "User One", "email": "one@test.io"})
        r2 = client.post("/users", json={"name": "User Two", "email": "two@test.io"})
        assert r2.json()["id"] > r1.json()["id"]

    def test_duplicate_email_returns_409(self, client):
        payload = {"name": "Alice", "email": "alice@test.io"}
        client.post("/users", json=payload)
        r = client.post("/users", json=payload)
        assert r.status_code == 409
        assert "already exists" in r.json()["detail"]

    def test_empty_name_returns_422(self, client):
        r = client.post("/users", json={"name": "   ", "email": "valid@test.io"})
        assert r.status_code == 422

    def test_missing_email_returns_422(self, client):
        r = client.post("/users", json={"name": "No Email"})
        assert r.status_code == 422


class TestListUsers:
    def test_list_users_empty_returns_total_zero(self, client):
        r = client.get("/users")
        assert r.status_code == 200
        assert r.json()["total"] == 0
        assert r.json()["users"] == []

    def test_list_users_returns_all_created_users(self, client):
        client.post("/users", json={"name": "User A", "email": "a@test.io"})
        client.post("/users", json={"name": "User B", "email": "b@test.io"})
        r = client.get("/users")
        assert r.json()["total"] == 2

    def test_list_users_response_shape(self, client):
        client.post("/users", json={"name": "Check Shape", "email": "shape@test.io"})
        users = client.get("/users").json()["users"]
        assert all("id" in u and "name" in u and "email" in u for u in users)


class TestGetSingleUser:
    def test_get_existing_user_returns_200(self, client):
        created_id = client.post("/users", json={"name": "Fetch Me", "email": "fetch@test.io"}).json()["id"]
        r = client.get(f"/users/{created_id}")
        assert r.status_code == 200
        assert r.json()["email"] == "fetch@test.io"

    def test_get_nonexistent_user_returns_404(self, client):
        r = client.get("/users/99999")
        assert r.status_code == 404
        assert "not found" in r.json()["detail"].lower()


class TestDeleteUser:
    def test_delete_existing_user_returns_200(self, client):
        user_id = client.post("/users", json={"name": "Delete Me", "email": "del@test.io"}).json()["id"]
        r = client.delete(f"/users/{user_id}")
        assert r.status_code == 200

    def test_deleted_user_no_longer_fetchable(self, client):
        user_id = client.post("/users", json={"name": "Gone", "email": "gone@test.io"}).json()["id"]
        client.delete(f"/users/{user_id}")
        r = client.get(f"/users/{user_id}")
        assert r.status_code == 404

    def test_delete_nonexistent_user_returns_404(self, client):
        r = client.delete("/users/99999")
        assert r.status_code == 404


class TestPrometheusMetrics:
    def test_metrics_endpoint_reachable(self, client):
        r = client.get("/metrics")
        assert r.status_code == 200

    def test_creating_user_increments_counter(self, client):
        from main import USERS_CREATED_TOTAL
        before = USERS_CREATED_TOTAL._value.get()
        client.post("/users", json={"name": "Count Me", "email": "count@test.io"})
        after = USERS_CREATED_TOTAL._value.get()
        assert after == before + 1
