from fastapi.testclient import TestClient
from src.api.datasetsharing.main import app
import pytest

client = TestClient(app)

@pytest.mark.order(1)
def test_health():

    response = client.get(
        "/api/v1/health",
    )

    assert response.status_code == 200
    assert response.json() == {"status": "UP"}