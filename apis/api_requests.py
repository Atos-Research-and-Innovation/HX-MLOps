import requests
import json

def test_add_model(url):
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

    endpoint = f"{url}/api/v1/model"

    parameters_json = json.dumps(test_data["parameters"])
    characteristics_json = json.dumps(test_data["characteristics"])

    test_file = {
        "file": ("model.pkl", b"dummy model content", "application/octet-stream")
    }

    data = {
        "name": test_data["name"],
        "version": test_data["version"],
        "status": test_data["status"],
        "library": test_data["library"],
        "libraryVersion": test_data["libraryVersion"],
        "domain": test_data["domain"],
        "tag": test_data["tag"],
        "parameters": parameters_json,
        "characteristics": characteristics_json,
    }

    response = requests.post(endpoint, data=data, files=test_file)

    assert response.status_code == 200, f"Request failed with status {response.status_code}"
    response_data = response.json()
    assert "modelIdentifier" in response_data, "Model ID not returned"
    print(response_data)


def test_health(url):
    endpoint = f"{url}/api/v1/health"

    response = requests.get(endpoint)

    assert response.status_code == 200, f"Request failed with status {response.status_code}"
    assert response.json() == {"status": "UP"}, f"Expected response {'status': 'UP'}, but got {response.json()}"
    print(response.json())

def test_get_model(url):
    model_id = 1
    version = "1.0"

    endpoint = f"{url}/api/v1/model/by_id/{model_id}?version={version}"
    
    response = requests.get(endpoint)

    assert response.status_code == 200, f"Request failed with status {response.status_code}"

    assert response.headers["Content-Type"] == "application/octet-stream", \
        f"Expected 'application/octet-stream', but got {response.headers['Content-Type']}"

    assert len(response.content) > 0, "The file content is empty"

    print(f"Received {len(response.content)} bytes of data")


    with open("downloaded_model.pkl", "wb") as f:
        f.write(response.content)


def test_get_model_catalog(url):

    data_params = {
        "tag": "beta",
        "status": "production",
        "domain": "text"
    }

    # data_params = {
    #     "tag": "",
    #     "status": "",
    #     "domain": ""
    # }

    endpoint = f"{url}/api/v1/model_catalog/"
    
    response = requests.get(endpoint, params=data_params)
    print(response.content)

    # assert response.status_code == 200, f"Request failed with status {response.status_code}"


if __name__ == "__main__":

    # url = "http://localhost/modelsharing/"
    url = "http://localhost:8080"

    # test_health(url)
    # test_add_model(url)
    # test_get_model(url)
    test_get_model_catalog(url)