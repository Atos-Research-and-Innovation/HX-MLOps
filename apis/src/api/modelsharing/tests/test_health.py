from fastapi.testclient import TestClient
from src.api.modelsharing.main import app
import pytest

client = TestClient(app)

@pytest.mark.order(1)
def test_health():

    test_file = ("model.pkl", b"dummy model content", "application/octet-stream")

    response = client.get(
        "/api/v1/health",
    )

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}