from fastapi.testclient import TestClient
from src.api.datasetsharing.main import app
import json
import pytest
from pathlib import Path

client = TestClient(app)


@pytest.mark.order(3)
def test_get_dataset():
    
    dataset_id = 1
    version = "1.0.0"
    print(dataset_id, version)

    response = client.get(f"/api/v1/dataset/by_id/{dataset_id}?version={version}")
    
    print(response.text)
    assert response.status_code == 200
    
    assert response.headers["Content-Type"] == "application/zip"
    
    assert len(response.content) > 0