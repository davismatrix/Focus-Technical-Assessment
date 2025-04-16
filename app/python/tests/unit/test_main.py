from fastapi.testclient import TestClient
from app.python.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}

def test_readiness_check():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"ready": "ok"}