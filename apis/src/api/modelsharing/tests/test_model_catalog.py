from fastapi.testclient import TestClient
from src.api.modelsharing.main import app
import json
import pytest
from pathlib import Path

client = TestClient(app)

@pytest.mark.order(4)
def test_get_model_catalog():

    response = client.get(
        "/api/v1/model_catalog"
    )
    print(response.text)
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "models" in response_data
    assert len(response_data["models"]) > 0