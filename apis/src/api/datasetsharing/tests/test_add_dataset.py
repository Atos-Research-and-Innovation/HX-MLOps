from fastapi.testclient import TestClient
from src.api.datasetsharing.main import app
from src.core.timescaledb import operations as db_operations
import json
from pathlib import Path
import pytest
from src.api.datasetsharing.database.model import Base as datasetsharingBase
from io import BytesIO

client = TestClient(app)

@pytest.mark.order(2)
def test_add_dataset():
    test_data = {
        "name": "ispm_dataset",
        "version": "1.0.0",
        "dataType": "mixed",
        "tag": "timeseries",
        "parameters": {
            "size": "350MB",
            "columns": "date/node_1/node_2/node_3",
            "row_number": "5000",
        },
    }

    db_operations.reset_database(datasetsharingBase)

    parameters_json = json.dumps(test_data["parameters"])


    csv_content = "id,name,value\n1,Item1,10.5\n2,Item2,20.3\n3,Item3,15.0"
    txt_content = "Model configuration: version 1.0\nParameter1: Value1\nParameter2: Value2"

    csv_file = BytesIO(csv_content.encode('utf-8'))
    txt_file = BytesIO(txt_content.encode('utf-8'))
    dataset_file = ("dataset.csv", csv_file, "text/csv")
    dataModel_file = ("dataModel.txt", txt_file, "text/plain")


    response = client.post(
        "/api/v1/dataset/", 
        data={
            "name": test_data["name"],
            "version": test_data["version"],
            "dataType": test_data["dataType"],
            "tag": test_data["tag"],
            "parameters": parameters_json,
        },
        files={
        "dataModelFile": dataModel_file,
        "datasetFile": dataset_file,
    }
    )
    print(response.text)

    assert response.status_code == 200, f"Request failed with status {response.status_code}"
    assert "datasetIdentifier" in response.json(), "Dataset ID not returned"




   