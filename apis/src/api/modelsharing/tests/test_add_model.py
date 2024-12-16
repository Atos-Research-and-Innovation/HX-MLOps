from fastapi.testclient import TestClient
from src.api.modelsharing.main import app
from src.core.timescaledb import operations as db_operations
import json
from pathlib import Path
import pytest
from src.api.modelsharing.database.model import Base as modelsharingBase

client = TestClient(app)

@pytest.mark.order(2)
def test_add_model():
    test_data = {
        "name": "test_model",
        "version": "1.0",
        "status": "production",
        "library": "sklearn",
        "libraryVersion": "0.24",
        "domain": "text",
        "tag": "beta",
        "parameters": {"param1": "value1", "param2": "value2"},
        "characteristics": {"param1": "value1", "param2": "value2"}
    }

    # restore database
    db_operations.reset_database(modelsharingBase)

    # Serialize the parameters and characteristics to JSON strings
    parameters_json = json.dumps(test_data["parameters"])
    characteristics_json = json.dumps(test_data["characteristics"])

    # Open the file for the test
    test_file = ("file", ("model.pkl", b"dummy model content", "application/octet-stream"))

    # Make the request to the FastAPI endpoint
    response = client.post(
        "/api/v1/model",  # Replace with your correct endpoint
        data={
            "name": test_data["name"],
            "version": test_data["version"],
            "status": test_data["status"],
            "library": test_data["library"],
            "libraryVersion": test_data["libraryVersion"],
            "domain": test_data["domain"],
            "tag": test_data["tag"],
            "parameters": parameters_json,
            "characteristics": characteristics_json,
        },
        files={test_file}
    )

    # Check the response status code and content
    assert response.status_code == 200, f"Request failed with status {response.status_code}"
    assert "modelIdentifier" in response.json(), "Model ID not returned"




   