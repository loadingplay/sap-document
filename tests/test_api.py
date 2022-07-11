from unittest.mock import Mock, patch
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.exceptions import JoinJsonSapError
import unittest
from app.sap_creditnote import SapCreditNote


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


class SapApiTestCase(unittest.TestCase):
    @patch("api.ConvertSapDocument")
    def test_post_sap_document_39(self, mock_sap_document):
        # definimos un cliente para hacer las peticiones
        client = TestClient(api)
        input_data = {
            "order": {
                "order": "test-1"
            },
            "sap_json": {
                "config": {
                    "type_document": "39"
                }
            }
        }
        expected_ouput = {'status': 'success', 'type': 'sap_document'}
        # Caso 1:
        # hacemos la peticion y verificamos que el codigo de respuesta sea 200

        # mock_sap_document = Mock()
        mock_sap_document.return_value.join_json_sap.return_value = {
            "status": "success",
            "type": "sap_document"
            }
        mock_sap_document.return_value.validate_article_in_sap.return_value = {
            "status": "success",
            "type": "sap_document"
            }
        result = client.post("/v1/generate_document", json=input_data)

        assert result.status_code == 200
        assert result.json() == expected_ouput

    @patch("api.SapCreditNote")
    def test_post_sap_document_credit_note(self, mock_credit_note):
        # definimos un cliente para hacer las peticiones
        client = TestClient(api)
        input_data = {
            "order": {
                "id": "test-1"
            },
            "sap_json": {
                "config": {
                    "type_document": "13"
                }
            }
        }
        expected_ouput = {'status': 'success', 'type': 'credit_note'}
        # Caso 1:
        # hacemos la peticion y verificamos que el codigo de respuesta sea 200

        # mock_sap_document = Mock()
        mock_credit_note.return_value.build_credit_note.return_value = {
            "status": "success",
            "type": "credit_note"
            }
        mock_credit_note.return_value.send_credit_note.return_value = {
            "status": "success",
            "type": "credit_note"
            }
        result = client.post("/v1/generate_document", json=input_data)

        assert result.status_code == 200
        assert result.json() == expected_ouput

    @patch("api.SapCreditNote")
    def test_post_sap_faliure(self, mock_credit_note):
        # definimos un cliente para hacer las peticiones

        client = TestClient(api)
        input_data = {
            "order": {
                "id": "test-1"
            },
            "sap_json": {
                "config": {
                    "type_document": "13"
                }
            }
        }
        expected_ouput = {'detail': 'Error on post workflows'}
        mock_credit_note.side_effect = HTTPException(
            status_code=500,
            detail="Error on post workflows"
        )
        # Caso 2:
        # hacemos la peticion y verificamos que el codigo de respuesta sea 500
        result = client.post("/v1/generate_document", json=input_data)
        assert result.status_code == 500
        assert result.json() == expected_ouput
