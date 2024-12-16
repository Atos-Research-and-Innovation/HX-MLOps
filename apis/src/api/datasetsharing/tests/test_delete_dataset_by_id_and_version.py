from fastapi.testclient import TestClient
from src.api.datasetsharing.main import app
import json
import pytest

client = TestClient(app)


@pytest.mark.order(6)
def test_delete_dataset():
    dataset_id = 1
    version = "1.0.0"

    response = client.delete(f"/api/v1/dataset/{dataset_id}?version={version}")
    print(response.text)
    assert response.status_code == 200

    data = response.json()
    print(data)
    assert data["datasetIdentifier"] == dataset_id