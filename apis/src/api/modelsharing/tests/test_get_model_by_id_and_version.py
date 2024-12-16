from fastapi.testclient import TestClient
from src.api.modelsharing.main import app
import json
import pytest
from pathlib import Path

client = TestClient(app)


@pytest.mark.order(3)
def test_get_model():
    
    model_id = 1
    version = "1.0"
    print(model_id, version)
    # Hacer la petición al endpoint
    response = client.get(f"/api/v1/model/by_id/{model_id}?version={version}")
    
    print(response.text)
    # Verificar que la respuesta es exitosa
    assert response.status_code == 200
    
    # Verificar que el contenido de la respuesta es el esperado (en este caso un archivo binario)
    assert response.headers["Content-Type"] == "application/octet-stream"
    
    # Comprobar que el contenido del archivo no está vacío
    assert len(response.content) > 0