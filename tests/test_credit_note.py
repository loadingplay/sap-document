import unittest
from unittest.mock import patch
from app.sap_creditnote import SapCreditNote


class SapCreditNoteTestCase(unittest.TestCase):
    @patch("app.sap_creditnote.SapCreditNote.get_linenum")
    def test_generate_document_lines(self, mock_get_linenum):
        input_data = {
            "order": {
                "extra_info": {
                    "name": "#67083",
                    "bill_comment": "Pedido Shopify: #67083",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 23726779957437,
                    "processing_method": "offsite",
                    "currency": "CLP",
                    "boleta_sap": {
                        "url": "https:test.pdf",
                        "folio": "143636",
                        "DocEntry": 59586
                    }
                },
            },
            "sap_json": {
                "config": {
                    "type_document": "39",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        linenum = [0, 1, 2, 3]
        send_data = SapCreditNote(input_data)
        mock_get_linenum.return_value = linenum
        result = send_data.generate_document_lines()
        expected_ouput = [
            {'BaseEntry': '59586', 'BaseLine': '0', 'BaseType': '13'},
            {'BaseEntry': '59586', 'BaseLine': '1', 'BaseType': '13'},
            {'BaseEntry': '59586', 'BaseLine': '2', 'BaseType': '13'},
            {'BaseEntry': '59586', 'BaseLine': '3', 'BaseType': '13'}]

        assert result == expected_ouput

    @patch("app.sap_creditnote.requests.Session.get")
    @patch("app.sap_creditnote.requests.Session.post")
    def test_get_linenum(self, mock_requests, mock_requests_get):
        input_data = {
            "order": {
                "extra_info": {
                    "name": "#67083",
                    "bill_comment": "Pedido Shopify: #67083",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 23726779957437,
                    "processing_method": "offsite",
                    "currency": "CLP",
                    "boleta_sap": {
                        "url": "https:test.pdf",
                        "folio": "143636",
                        "DocEntry": 59586
                    }
                },
            },
            "sap_json": {
                "config": {
                    "type_document": "39",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        return_login_sap = {
            "status": "success",
            "DocumentLines": [
                {"LineNum": 0, "ItemCode": "x"},
                {"LineNum": 1, "ItemCode": "x"},
                {"LineNum": 2, "ItemCode": "x"},
                {"LineNum": 3, "ItemCode": "x"}
            ]
            }
        send_data = SapCreditNote(input_data)
        mock_requests.return_value = return_login_sap
        mock_requests_get.return_value.json.return_value = return_login_sap
        result = send_data.get_linenum()
        expected_ouput = [0, 1, 2, 3]

        assert result == expected_ouput

    @patch("app.sap_creditnote.SapCreditNote.generate_document_lines")
    def test_build_credit_note(self, mock_generate_document_lines):
        input_data = {
            "order": {
                "customer": {
                    "id": 72235112,
                    "name": "test",
                    "rut": "",
                    "last_name": "Morales"
                },
                "extra_info": {
                    "name": "#67083",
                    "bill_comment": "Pedido Shopify: #67083",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 23726779957437,
                    "processing_method": "offsite",
                    "currency": "CLP",
                    "boleta_sap": {
                        "url": "https:test.pdf",
                        "folio": "143636",
                        "DocEntry": 59586
                    }
                },
            },
            "sap_json": {
                "config": {
                    "type_document": "39",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        document_line = [
                {'BaseEntry': '59586', 'BaseLine': '0', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '1', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '2', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '3', 'BaseType': '13'}
            ]
        send_data = SapCreditNote(input_data)
        mock_generate_document_lines.return_value = document_line
        result = send_data.build_credit_note()
        expected_ouput = {
            'CardCode': 'C77777777-7',
            'DocumentLines': [
                {'BaseEntry': '59586', 'BaseLine': '0', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '1', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '2', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '3', 'BaseType': '13'}
            ]
        }

        assert result == expected_ouput

    @patch("app.sap_creditnote.requests.post")
    @patch("app.sap_creditnote.SapCreditNote.build_credit_note")
    def test_send_credit_note(self, mock_build_credit_note, mock_request_post):
        input_data = {
            "order": {
                "customer": {
                    "id": 72235112,
                    "name": "test",
                    "rut": "",
                    "last_name": "Morales"
                },
                "extra_info": {
                    "name": "#67083",
                    "bill_comment": "Pedido Shopify: #67083",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 23726779957437,
                    "processing_method": "offsite",
                    "currency": "CLP",
                    "boleta_sap": {
                        "url": "https:test.pdf",
                        "folio": "143636",
                        "DocEntry": 59586
                    }
                },
            },
            "sap_json": {
                "config": {
                    "type_document": "39",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        build_json = {
            'CardCode': 'C77777777-7',
            'DocumentLines': [
                {'BaseEntry': '59586', 'BaseLine': '0', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '1', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '2', 'BaseType': '13'},
                {'BaseEntry': '59586', 'BaseLine': '3', 'BaseType': '13'}
            ]
        }
        response_credit_note = {"status": "success"}
        send_data = SapCreditNote(input_data)
        mock_build_credit_note.return_value = build_json
        mock_request_post.return_value.json.return_value = response_credit_note
        result = send_data.send_credit_note()
        expected_ouput = {"status": "success"}

        assert result == expected_ouput
