from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_role_matrix_endpoint() -> None:
    response = client.get("/api/auth/role-matrix")
    assert response.status_code == 200
    payload = response.json()
    assert "roles" in payload
    assert any(role["role"] == "College Administrator" for role in payload["roles"])


def test_seed_endpoint() -> None:
    response = client.post("/api/setup/seed")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "seeded"
    assert payload["student_count"] >= 150


def test_student_score_endpoint() -> None:
    client.post("/api/setup/seed")
    response = client.get("/api/students")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 150
    assert "final_score" in payload[0]["score"]
