from unittest.mock import patch
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.exceptions import JoinJsonSapError


from api import api
# Casos de prueba:
# 1.- Enviar un documento y que responda 200(Caso exitoso)
# 2.- Enviar un documento y que responda 500(Caso fallido)
 
# Flujo Caso 1:
# Entrada Esperada: Diccionario con la orden y la config de sap
# Salida Esperada: status 20

# Flujo Caso 2:
# Entrada Esperada: Diccionario con la orden y la config de sap
# Salida Esperada: error 500

@patch("api.ConvertSapDocument")
def test_post_sap_success(mock_convert_sap_document):
    # definimos un cliente para hacer las peticiones
    client = TestClient(api)
    input_data = {
        "order": {},
        "sap_json": {
            "config": {}
        }
    }
    expected_ouput = {}

    # Caso 1:
    # hacemos la peticion y verificamos que el codigo de respuesta sea 200
    result = client.post("/v1/generate_document", json=input_data)
    assert result.status_code == 200
    assert result.json() == expected_ouput

@patch("api.ConvertSapDocument")
def test_post_sap_faliure(mock_convert_sap_document):
    # definimos un cliente para hacer las peticiones

    client = TestClient(api)
    input_data = {
        "order": {},
        "sap_json": {
            "config": {}
        }
    }
    expected_ouput = {'detail': 'Error on post workflows'}
    mock_convert_sap_document.side_effect = HTTPException(
        status_code=500,
        detail="Error on post workflows"
    )
    # Caso 2:
    # hacemos la peticion y verificamos que el codigo de respuesta sea 500
    result = client.post("/v1/generate_document", json=input_data)
    assert result.status_code == 500
    assert result.json() == expected_ouput

@patch("api.ConvertSapDocument")
def test_post_sap_faliure_400(mock_convert_sap_document):
    # definimos un cliente para hacer las peticiones

    client = TestClient(api)
    input_data = {
        "order": {},
        "sap_json": {
            "config": {}
        }
    }
    expected_ouput = {'detail': 'Error on data conversion'}
    mock_convert_sap_document.return_value.join_json_sap.side_effect = JoinJsonSapError("error")
    
    # Caso 2:
    # hacemos la peticion y verificamos que el codigo de respuesta sea 500
    result = client.post("/v1/generate_document", json=input_data)
    assert result.status_code == 400
    assert result.json() == expected_ouput
    

