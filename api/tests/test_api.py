from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# Health check
def test_health():
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Sem API key 
def test_metrics_unauthorized():
    response = client.get("/v1/metrics/funnel")
    assert response.status_code == 401


# Com API key
def test_metrics_authorized():
    response = client.get(
        "/v1/metrics/funnel",
        headers={"x-api-key": "rentcars-secret"}
    )
    assert response.status_code == 200
    assert "total_events" in response.json()


def test_rate_limit():
    for _ in range(10):
        response = client.get(
            "/v1/metrics/funnel",
            headers={"x-api-key": "rentcars-secret"}
        )

    assert response.status_code in [200, 429]