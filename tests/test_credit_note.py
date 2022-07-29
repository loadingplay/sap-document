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
                        "url": "https://archivos.febos.io/temporal/1658925380042/E76195762-7_39_428.0.pdf",  # noqa
                        "folio": "428",
                        "DocEntry": 225296
                    }
                },
                "products": [
                    {
                        "id": 1205434,
                        "quantity": 1.0,
                        "subtotal": 11990.0,
                        "price": 11990.0,
                        "combination": "",
                        "sku": "21025",
                        "name": "Jockey Conguillio Lino Blanco",
                        "discount": 0.0,
                    },
                    {
                        "id": 1205435,
                        "quantity": 1.0,
                        "subtotal": 7990.0,
                        "order_id": 618597,
                        "price": 7990.0,
                        "sku": "60483",
                        "name": "Gorro Ribbed Reciclado Fit Medio Naranjo",
                        "discount": 0.0,
                    },
                    {
                        "id": 1205436,
                        "quantity": 1.0,
                        "subtotal": 12990.0,
                        "price": 12990.0,
                        "sku": "20590",
                        "name": "Cinturón WL Camo Elasticado - Verde",
                        "discount": 0.0,
                    }
                ],
            },
            "sap_json": {
                "type": "sap credit note",
                "config": {
                    "type_document": "61",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "lamawild-sap",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        linenum = [
            {"lineNum": 0, "quantity": 1.0},
            {"lineNum": 1, "quantity": 1.0},
            {"lineNum": 2, "quantity": 1.0},
            {"lineNum": 3, "quantity": 1.0}
        ]
        send_data = SapCreditNote(input_data)
        mock_get_linenum.return_value = linenum
        result = send_data.generate_document_lines()
        expected_ouput = [
            {
                'BaseEntry': '225296',
                'BaseLine': '0',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '1',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '2',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '3',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            }
        ]

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
                {"LineNum": 0, "Quantity": 1.0},
                {"LineNum": 1, "Quantity": 1.0},
                {"LineNum": 2, "Quantity": 1.0},
                {"LineNum": 3, "Quantity": 1.0}
            ]
            }
        send_data = SapCreditNote(input_data)
        mock_requests.return_value = return_login_sap
        mock_requests_get.return_value.json.return_value = return_login_sap
        result = send_data.get_linenum()
        expected_ouput = [
            {"lineNum": 0, "quantity": 1.0},
            {"lineNum": 1, "quantity": 1.0},
            {"lineNum": 2, "quantity": 1.0},
            {"lineNum": 3, "quantity": 1.0}
        ]

        assert result == expected_ouput

    @patch("app.sap_creditnote.SapCreditNote.get_order")
    @patch("app.sap_creditnote.SapCreditNote.get_user")
    def test_build_credit_note(self, mock_get_user, mock_get_order):
        get_user = {'Password': '1234', 'UserName': 'test_user'}
        get_order = {
            "U_SEI_IDPS": "lamawild-sap-test-#95067",
            "DocDate": "2022-07-27T11:09:59.268092",
            "DocDueDate": "2022-07-27T11:09:59.268092",
            "TaxDate": "2022-07-27T11:09:59.268092",
            "CardCode": "77777777-7C",
            "DocCurrency": "CLP",
            "DocRate": 1,
            "SalesPersonCode": 4,
            "ContactPersonCode": "null",
            "U_SEI_MAILCLIENTE": "barbaraottonelapostol@gmail.com",
            "FederalTaxID": "77777777-7",
            "Indicator": "61",
            "U_SEI_FOREF": "#95067",
            "U_SEI_FEREF": "2022-07-27T11:09:59.268092",
            "U_SEI_INREF": 33,
            "U_SEI_CREF": 1,
            "U_SEI_CANAL": "CAN03",
            "U_SEI_ESTADOPAGO": "Pagado",
            "U_SEI_FEBOSID": "",
            "DocumentLines": [
                {
                    "BaseEntry": "225301",
                    "BaseLine": "0",
                    "BaseType": "13",
                    "BatchNumbers": [
                        {
                            "BatchNumber": "shopify",
                            "Quantity": 1.0
                        }
                    ]
                },
                {
                    "BaseEntry": "225301",
                    "BaseLine": "1",
                    "BaseType": "13",
                    "BatchNumbers": [
                        {
                            "BatchNumber": "shopify",
                            "Quantity": 1.0
                        }
                    ]
                }
            ]
        }
        send_data = SapCreditNote("")
        mock_get_user.return_value = get_user
        mock_get_order.return_value = get_order
        result = send_data.build_credit_note()
        expected_ouput = {
            "User": {
                "Password": "1234",
                "UserName": "test_user"
            },
            "Order": {
                "U_SEI_IDPS": "lamawild-sap-test-#95067",
                "DocDate": "2022-07-27T11:09:59.268092",
                "DocDueDate": "2022-07-27T11:09:59.268092",
                "TaxDate": "2022-07-27T11:09:59.268092",
                "CardCode": "77777777-7C",
                "DocCurrency": "CLP",
                "DocRate": 1,
                "SalesPersonCode": 4,
                "ContactPersonCode": "null",
                "U_SEI_MAILCLIENTE": "barbaraottonelapostol@gmail.com",
                "FederalTaxID": "77777777-7",
                "Indicator": "61",
                "U_SEI_FOREF": "#95067",
                "U_SEI_FEREF": "2022-07-27T11:09:59.268092",
                "U_SEI_INREF": 33,
                "U_SEI_CREF": 1,
                "U_SEI_CANAL": "CAN03",
                "U_SEI_ESTADOPAGO": "Pagado",
                "U_SEI_FEBOSID": "",
                "DocumentLines": [
                    {
                        "BaseEntry": "225301",
                        "BaseLine": "0",
                        "BaseType": "13",
                        "BatchNumbers": [
                            {
                                "BatchNumber": "shopify",
                                "Quantity": 1.0
                            }
                        ]
                    },
                    {
                        "BaseEntry": "225301",
                        "BaseLine": "1",
                        "BaseType": "13",
                        "BatchNumbers": [
                            {
                                "BatchNumber": "shopify",
                                "Quantity": 1.0
                            }
                        ]
                    }
                ]
            }
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
            "User": {
                "Password": "1234",
                "UserName": "test_user"
            },
            "Order": {
                "U_SEI_IDPS": "lamawild-sap-test-#95067",
                "DocDate": "2022-07-27T11:09:59.268092",
                "DocDueDate": "2022-07-27T11:09:59.268092",
                "TaxDate": "2022-07-27T11:09:59.268092",
                "CardCode": "77777777-7C",
                "DocCurrency": "CLP",
                "DocRate": 1,
                "SalesPersonCode": 4,
                "ContactPersonCode": "null",
                "U_SEI_MAILCLIENTE": "barbaraottonelapostol@gmail.com",
                "FederalTaxID": "77777777-7",
                "Indicator": "61",
                "U_SEI_FOREF": "#95067",
                "U_SEI_FEREF": "2022-07-27T11:09:59.268092",
                "U_SEI_INREF": 33,
                "U_SEI_CREF": 1,
                "U_SEI_CANAL": "CAN03",
                "U_SEI_ESTADOPAGO": "Pagado",
                "U_SEI_FEBOSID": "",
                "DocumentLines": [
                    {
                        "BaseEntry": "225301",
                        "BaseLine": "0",
                        "BaseType": "13",
                        "BatchNumbers": [
                            {
                                "BatchNumber": "shopify",
                                "Quantity": 1.0
                            }
                        ]
                    },
                    {
                        "BaseEntry": "225301",
                        "BaseLine": "1",
                        "BaseType": "13",
                        "BatchNumbers": [
                            {
                                "BatchNumber": "shopify",
                                "Quantity": 1.0
                            }
                        ]
                    }
                ]
            }
        }
        response_credit_note = {"status": "success"}
        send_data = SapCreditNote(input_data)
        mock_build_credit_note.return_value = build_json
        mock_request_post.return_value.json.return_value = response_credit_note
        result = send_data.send_credit_note()
        expected_ouput = {"status": "success"}

        assert result == expected_ouput

    @patch("app.sap_creditnote.SapCreditNote.generate_document_lines")
    def test_get_document_lines_with_BatchNumbers_success(
            self, mock_generate_document_lines):
        input_data = {
            "order": {
                "site_name": "lamawild-sap",
            },
            "sap_json": {
                "type": "sap credit note",
                "config": {
                    "type_document": "61",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "lamawild-sap",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        document_lines = [
            {
                'BaseEntry': '225296',
                'BaseLine': '0',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0
                }]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '1',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '2',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '3',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            }]
        send_data = SapCreditNote(input_data)
        mock_generate_document_lines.return_value = document_lines
        result = send_data.get_document_lines_batch()
        expected_ouput = [
            {
                'BaseEntry': '225296',
                'BaseLine': '0',
                'BaseType': '13',
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '1',
                'BaseType': '13',
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '2',
                'BaseType': '13',
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '3',
                'BaseType': '13',
            }]

        assert result == expected_ouput

    @patch("app.sap_creditnote.SapCreditNote.generate_document_lines")
    def test_get_document_lines_with_BatchNumbers_failled(
            self, mock_generate_document_lines):
        input_data = {
            "order": {
                "site_name": "wildfoods-sap",
            },
            "sap_json": {
                "type": "sap credit note",
                "config": {
                    "type_document": "61",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "lamawild-sap",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        document_lines = [
            {
                'BaseEntry': '225296',
                'BaseLine': '0',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0
                }]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '1',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '2',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '3',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            }]

        send_data = SapCreditNote(input_data)
        mock_generate_document_lines.return_value = document_lines
        result = send_data.get_document_lines_batch()
        expected_ouput = [
            {
                'BaseEntry': '225296',
                'BaseLine': '0',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0
                }]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '1',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '2',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            },
            {
                'BaseEntry': '225296',
                'BaseLine': '3',
                'BaseType': '13',
                'BatchNumbers': [{
                    'BatchNumber': 'shopify',
                    'Quantity': 1.0}]
            }]

        assert result == expected_ouput

    @patch("app.sap_creditnote.SapCreditNote.get_document_lines_batch")
    def test_get_order(self, mock_get_document_lines_batch):
        input_data = {
            "order": {
                "id": 618618,
                "date": "2022-07-27T11:09:59.268092",
                "type": 1,
                "subtotal": 34990.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1": "Avenida Ossa 1806 Avenida Ossa 1806",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "La Reina",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 37980.0,
                "items_quantity": "None",
                "products_quantity": "None",
                "billing_id": 26635455,
                "shipping_id": 26635455,
                "payment_type": "shopify",
                "source": "",
                "voucher": "",
                "tracking_code": "",
                "provider_id": "None",
                "site_id": "None",
                "extra_info": {
                    "name": "#95067",
                    "bill_comment": "Pedido Shopify: #95067",
                    "payment_gateway": [
                        "mercado_pago"
                    ],
                    "checkout_id": 25432180523197,
                    "processing_method": "offsite",
                    "currency": "CLP",
                    "product_not_found": [
                        "21MCAMDENHWAS"
                    ],
                    "boleta_sap": {
                        "url": "https://archivos.febos.io/temporal/1658934635650/E76195762-7_39_430.0.pdf",  # noqa
                        "folio": "430",
                        "DocEntry": 225301
                    }
                },
                "name": "",
                "reference_code": "",
                "adjustment": 0.0,
                "origin": "shopify",
                "url_document": "https://archivos.febos.io/temporal/1658934635650/E76195762-7_39_430.0.pdf",  # noqa
                "site_name": "workflows",
                "status": "cancelado",
                "discount_code": "",
                "customer_id": 2787776,
                "cellar_id": 720,
                "products": [
                    {
                        "id": 1205485,
                        "quantity": 1.0,
                        "subtotal": 34990.0,
                        "order_id": 618618,
                        "size": "",
                        "price": 34990.0,
                        "combination": "",
                        "sku": "21MCAMDENHWAS",
                        "name": "Camisa Denim Algodón Orgánico Hombre Gris",
                        "discount": 0.0,
                        "barcode": "",
                        "cellar_id": "2323"
                    }
                ],
                "customer": {
                    "id": 26635455,
                    "name": "Barbara",
                    "email": "barbaraottonelapostol@gmail.com",
                    "address": "Avenida Ossa 1806 Avenida Ossa 1806",
                    "telephone": "9 7135 3837",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "La Reina",
                    "region": "Santiago",
                    "customer_id": 2787776,
                    "last_name": "Ottone"
                },
                "wf": "f45978bf"
            },
            "sap_json": {
                "type": "sap credit note",
                "config": {
                    "type_document": "61",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "lamawild-sap-test",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        document_lines_batch = [
            {
                "BaseEntry": "225301",
                "BaseLine": "0",
                "BaseType": "13",
                "BatchNumbers": [
                    {
                        "BatchNumber": "shopify",
                        "Quantity": 1.0
                    }
                ]
            },
            {
                "BaseEntry": "225301",
                "BaseLine": "1",
                "BaseType": "13",
                "BatchNumbers": [
                    {
                        "BatchNumber": "shopify",
                        "Quantity": 1.0
                    }
                ]
            }]

        send_data = SapCreditNote(input_data)
        mock_get_document_lines_batch.return_value = document_lines_batch
        result = send_data.get_order()
        expected_ouput = {
                "U_SEI_IDPS": "lamawild-sap-test-#95067",
                "DocDate": "2022-07-27T11:09:59.268092",
                "DocDueDate": "2022-07-27T11:09:59.268092",
                "TaxDate": "2022-07-27T11:09:59.268092",
                "CardCode": "77777777-7C",
                "DocCurrency": "CLP",
                "DocRate": 1,
                "SalesPersonCode": 4,
                "ContactPersonCode": "null",
                "U_SEI_MAILCLIENTE": "barbaraottonelapostol@gmail.com",
                "FederalTaxID": "77777777-7",
                "Indicator": "61",
                "U_SEI_FOREF": "#95067",
                "U_SEI_FEREF": "2022-07-27T11:09:59.268092",
                "U_SEI_INREF": 33,
                "U_SEI_CREF": 1,
                "U_SEI_CANAL": "CAN03",
                "U_SEI_ESTADOPAGO": "Pagado",
                "U_SEI_FEBOSID": "",
                "DocumentLines": [
                    {
                        "BaseEntry": "225301",
                        "BaseLine": "0",
                        "BaseType": "13",
                        "BatchNumbers": [
                            {
                                "BatchNumber": "shopify",
                                "Quantity": 1.0
                            }
                        ]
                    },
                    {
                        "BaseEntry": "225301",
                        "BaseLine": "1",
                        "BaseType": "13",
                        "BatchNumbers": [
                            {
                                "BatchNumber": "shopify",
                                "Quantity": 1.0
                            }
                        ]
                    }
                ]
            }

        assert result == expected_ouput

    def test_get_user(self):
        input_data = {
            "sap_json": {
                "type": "sap credit note",
                "config": {
                    "type_document": "61",
                    "username": "test_user",
                    "password": "1234",
                    "site_name": "lamawild-sap",
                    "WarehouseCode": "",
                    "company_db": "",
                    "site_url": "",
                    "access_token_lp": ""
                }
            }
        }
        send_data = SapCreditNote(input_data)
        result = send_data.get_user()
        expected_ouput = {'Password': '1234', 'UserName': 'test_user'}

        assert result == expected_ouput
