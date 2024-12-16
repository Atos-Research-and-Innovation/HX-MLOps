from fastapi.testclient import TestClient
from src.api.datasetsharing.main import app
import json
import pytest
from pathlib import Path

client = TestClient(app)

@pytest.mark.order(5)
def test_get_dataset_catalog():

    dataset_id = 1
    version = "1.0.0"

    response = client.get(f"/api/v1/dataset/{dataset_id}/data?version={version}")
    print(response.text)
    assert response.status_code == 200
    
    response_data = response.json()
    assert isinstance(response_data, dict)