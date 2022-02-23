from unittest.mock import patch
from app.convert_sap_document import ConvertSapDocument
import unittest


class ConvertSapDocumentTestCase(unittest.TestCase):
    def test_get_user_success(self):
        input_data = {
            "order": {},
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
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_user()
        expected_ouput = {
                    "Password": "1234",
                    "UserName": "test_user"
                }

        assert result == expected_ouput

    def test_get_product(self):
        input_data = {
            "order": {
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "combination": "",
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "cellar_id": "2342"
                    }
                ],
            },
            "sap_json": {
                "id": "204",
                "type": "sap document",
                "next_task": "end",
                "config": {
                    "type_document": "39",
                    "username": "LOGINPLAY",
                    "password": "1234",
                    "site_name": "wildfoods-sap",
                    "WarehouseCode": "BODECOMC",
                    "company_db": "TESTWF",
                    "site_url": "https",
                    "access_token_lp": "x"
                }
            }
        }
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_products()
        expected_ouput = [{
            "ItemCode": "30402",
            "TaxCode": "IVA",
            "Quantity": 6.0,
            "UnitPrice": 4193.277311,
            "WarehouseCode": "BODECOMC",
            "DiscountPercent": 0,
            "BatchNumbers": [
                {
                    "BatchNumber": "shopify",
                    "Quantity": 6.0
                }
            ]
            },
            {

                "ItemCode": "envio",
                "TaxCode": "IVA",
                "Quantity": 1,
                "WarehouseCode": "BODECOMC",
                "UnitPrice": 2512.61
            }
        ]

        assert result == expected_ouput

    def test_get_sn_success(self):
        input_data = {
            "order": {
                "id": 3825128,
                "date": "2022-02-14T09:12:44.716972",
                "type": 1,
                "subtotal": 29940.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 32930.0,
                "items_quantity": "None",
                "products_quantity": "None",
                "billing_id": 72542921,
                "shipping_id": 72542921,
                "payment_type": "shopify",
                "source": "",
                "voucher": "",
                "tracking_code": "",
                "provider_id": "None",
                "site_id": "None",
                "extra_info": {
                    "name": "#59942",
                    "bill_comment": "Pedido Shopify: #59942",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 24164719591620,
                    "processing_method": "offsite",
                    "currency": "CLP"
                },
                "name": "",
                "reference_code": "4356494033092",
                "deleted": False,
                "adjustment": -0.0,
                "origin": "shopify",
                "url_document": "",
                "site_name": "wildfoods",
                "status": "despachado",
                "discount_code": "",
                "customer_id": 12862185,
                "cellar_id": 2342,
                "status_counter": 0,
                "multicellar": False,
                "tags": "low-risk, no_superalimento, oficina, Online Store",
                "payments": [
                    {
                        "name": "PAGO_FACIL",
                        "amount": 32930.0
                    }
                ],
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "combination": "",
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "taxable": True,
                        "cellar_id": "2342"
                    }
                ],
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            }
        }
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_sn()
        expected_ouput = {
            "CardCode": "C77777777-7C",
            "CardName": "María Paz",
            "CardType": "cCustomer",
            "GroupCode": 100,
            "FederalTaxID": "77777777-7",
            "EmailAddress": "mperrazuriz@aptus.org",
            "CardForeignName": "Shopify",
            "ShipToDefault": "DESPACHO",
            "BilltoDefault": "FACTURACION",
            "U_SEI_GNRP": "GOBIERNO",
            "DebitorAccount": "110401001",
            "U_Tipo": "N",
            "Currency": "CLP",
            "BPAddresses": [
                {
                    "AddressName": "DESPACHO",
                    "Street": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "City": "chile",
                    "County": "Vitacura",
                    "Country": "CL",
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_ShipTo"
                },
                {
                    "AddressName": "FACTURACION",
                    "Street": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "City": "chile",
                    "County": "Vitacura",
                    "Country": "CL",
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_BillTo"
                }
            ],
            "ContactEmployees": [
                {
                    "Name": "María Paz Errazuriz",
                    "Phone1": "992825655",
                    "E_Mail": "mperrazuriz@aptus.org",
                    "FirstName": "María Paz",
                    "MiddleName": "null",
                    "LastName": "Errazuriz"
                }
            ]
        }

        assert result == expected_ouput

    def test_get_order(self):
        input_data = {
            "order": {
                "id": 3825128,
                "date": "2022-02-14T09:12:44.716972",
                "subtotal": 29940.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 32930.0,
                "extra_info": {
                    "name": "#59942",
                    "bill_comment": "Pedido Shopify: #59942",
                    "currency": "CLP"
                },
                "name": "",
                "reference_code": "4356494033092",
                "deleted": False,
                "adjustment": -0.0,
                "origin": "shopify",
                "url_document": "",
                "site_name": "wildfoods",
                "cellar_id": 2342,
                "payments": [
                    {
                        "name": "PAGO_FACIL",
                        "amount": 32930.0
                    }
                ],
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "combination": "",
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "taxable": True,
                        "cellar_id": "2342"
                    }
                ],
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            },
            "sap_json": {
                "id": "204",
                "type": "sap document",
                "next_task": "end",
                "config": {
                    "type_document": "39",
                    "username": "LOGINPLAY",
                    "password": "1234",
                    "site_name": "wildfoods-sap",
                    "WarehouseCode": "BODECOMC",
                    "company_db": "TESTWF",
                    "site_url": "https",
                    "access_token_lp": "x"
                }
            }
            }
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_order()
        expected_ouput = {
            "U_SEI_IDPS": "wildfoods-sap-#59942",
            "DocDate": "2022-02-14T09:12:44.716972",
            "DocDueDate": "2022-02-14T09:12:44.716972",
            "TaxDate": "2022-02-14T09:12:44.716972",
            "CardCode": "C77777777-7",
            "DocCurrency": "CLP",
            "DocRate": 1,
            "SalesPersonCode": 4,
            "ContactPersonCode": "null",
            "U_SEI_MAILCLIENTE": "mperrazuriz@aptus.org",
            "Indicator": "39",
            "FederalTaxID": "77777777-7",
            "U_SEI_FOREF": "#59942",
            "U_SEI_FEREF": "2022-02-14T09:12:44.716972",
            "U_SEI_INREF": 801,
            "U_SEI_CANAL": "CAN03",
            "DocumentLines": [
                {
                    "ItemCode": "30402",
                    "TaxCode": "IVA",
                    "Quantity": 6.0,
                    "UnitPrice": 4193.277311,
                    "WarehouseCode": "BODECOMC",
                    "DiscountPercent": 0,
                    "BatchNumbers": [
                        {
                            "BatchNumber": "shopify",
                            "Quantity": 6.0
                        }
                    ]
                },
                {
                    "ItemCode": "envio",
                    "TaxCode": "IVA",
                    "Quantity": 1,
                    "WarehouseCode": "BODECOMC",
                    "UnitPrice": 2512.61
                }
            ]
        }
        assert result == expected_ouput

    def test_order_not_U_SEI_ESTADOPAGO_for_lamawild_sap(self):
        input_data = {
            "order": {
                "id": 3825128,
                "date": "2022-02-14T09:12:44.716972",
                "subtotal": 29940.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 32930.0,
                "extra_info": {
                    "name": "#59942",
                    "bill_comment": "Pedido Shopify: #59942",
                    "currency": "CLP"
                },
                "reference_code": "4356494033092",
                "adjustment": -0.0,
                "origin": "shopify",
                "url_document": "",
                "site_name": "lamawild-sap",
                "cellar_id": 2342,
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "cellar_id": "2342"
                    }
                ],
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            },
            "sap_json": {
                "id": "204",
                "type": "sap document",
                "next_task": "end",
                "config": {
                    "type_document": "39",
                    "username": "LOGINPLAY",
                    "password": "1234",
                    "site_name": "lamawild-sap",
                    "WarehouseCode": "BODECOMC",
                    "company_db": "TESTWF",
                    "site_url": "https",
                    "access_token_lp": "x"
                }
            }
            }
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_order()
        expected_ouput = {
            "U_SEI_IDPS": "lamawild-sap-#59942",
            "DocDate": "2022-02-14T09:12:44.716972",
            "DocDueDate": "2022-02-14T09:12:44.716972",
            "TaxDate": "2022-02-14T09:12:44.716972",
            "CardCode": "C77777777-7",
            "DocCurrency": "CLP",
            "DocRate": 1,
            "SalesPersonCode": 4,
            "ContactPersonCode": "null",
            "U_SEI_MAILCLIENTE": "mperrazuriz@aptus.org",
            "Indicator": "39",
            "FederalTaxID": "77777777-7",
            "U_SEI_FOREF": "#59942",
            "U_SEI_FEREF": "2022-02-14T09:12:44.716972",
            "U_SEI_INREF": 801,
            "U_SEI_CANAL": "CAN03",
            "DocumentLines": [
                {
                    "ItemCode": "30402",
                    "TaxCode": "IVA",
                    "Quantity": 6.0,
                    "UnitPrice": 4193.277311,
                    "WarehouseCode": "BODECOMC",
                    "DiscountPercent": 0,
                },
                {
                    "ItemCode": "envio",
                    "TaxCode": "IVA",
                    "Quantity": 1,
                    "WarehouseCode": "BODECOMC",
                    "UnitPrice": 2512.61
                }
            ]
        }
        assert result == expected_ouput

    def test_order_U_SEI_ESTADOPAGO_for_wildfoods_sap(self):
        input_data = {
            "order": {
                "id": 3825128,
                "date": "2022-02-14T09:12:44.716972",
                "subtotal": 29940.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 32930.0,
                "extra_info": {
                    "name": "#59942",
                    "bill_comment": "Pedido Shopify: #59942",
                    "currency": "CLP"
                },
                "reference_code": "4356494033092",
                "adjustment": -0.0,
                "origin": "shopify",
                "url_document": "",
                "site_name": "wildfoods-sap",
                "cellar_id": 2342,
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "cellar_id": "2342"
                    }
                ],
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            },
            "sap_json": {
                "id": "204",
                "type": "sap document",
                "next_task": "end",
                "config": {
                    "type_document": "39",
                    "username": "LOGINPLAY",
                    "password": "1234",
                    "site_name": "wildfoods-sap",
                    "WarehouseCode": "BODECOMC",
                    "company_db": "TESTWF",
                    "site_url": "https",
                    "access_token_lp": "x"
                }
            }
            }
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_order()
        expected_ouput = {
            "U_SEI_IDPS": "wildfoods-sap-#59942",
            "DocDate": "2022-02-14T09:12:44.716972",
            "DocDueDate": "2022-02-14T09:12:44.716972",
            "TaxDate": "2022-02-14T09:12:44.716972",
            "CardCode": "C77777777-7",
            "DocCurrency": "CLP",
            "DocRate": 1,
            "SalesPersonCode": 4,
            "ContactPersonCode": "null",
            "U_SEI_MAILCLIENTE": "mperrazuriz@aptus.org",
            "Indicator": "39",
            "FederalTaxID": "77777777-7",
            "U_SEI_FOREF": "#59942",
            "U_SEI_FEREF": "2022-02-14T09:12:44.716972",
            "U_SEI_INREF": 801,
            "U_SEI_CANAL": "CAN03",
            "U_SEI_ESTADOPAGO": "Pagado",
            "DocumentLines": [
                {
                    "ItemCode": "30402",
                    "TaxCode": "IVA",
                    "Quantity": 6.0,
                    "UnitPrice": 4193.277311,
                    "WarehouseCode": "BODECOMC",
                    "DiscountPercent": 0,
                    "BatchNumbers": [
                        {
                            "BatchNumber": "shopify",
                            "Quantity": 6.0
                        }
                    ]
                },
                {
                    "ItemCode": "envio",
                    "TaxCode": "IVA",
                    "Quantity": 1,
                    "WarehouseCode": "BODECOMC",
                    "UnitPrice": 2512.61
                }
            ]
        }
        assert result == expected_ouput

    def test_join_json_sap(self):
        input_data = {
            "order": {
                "id": 3825128,
                "date": "2022-02-14T09:12:44.716972",
                "type": 1,
                "subtotal": 29940.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 32930.0,
                "items_quantity": "None",
                "products_quantity": "None",
                "billing_id": 72542921,
                "shipping_id": 72542921,
                "payment_type": "shopify",
                "source": "",
                "voucher": "",
                "tracking_code": "",
                "provider_id": "None",
                "site_id": "None",
                "extra_info": {
                    "name": "#59942",
                    "bill_comment": "Pedido Shopify: #59942",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 24164719591620,
                    "processing_method": "offsite",
                    "currency": "CLP"
                },
                "name": "",
                "reference_code": "4356494033092",
                "deleted": False,
                "adjustment": -0.0,
                "origin": "shopify",
                "url_document": "",
                "site_name": "wildfoods",
                "status": "despachado",
                "discount_code": "",
                "customer_id": 12862185,
                "cellar_id": 2342,
                "status_counter": 0,
                "multicellar": False,
                "tags": "low-risk, no_superalimento, oficina, Online Store",
                "payments": [
                    {
                        "name": "PAGO_FACIL",
                        "amount": 32930.0
                    }
                ],
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "combination": "",
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "taxable": True,
                        "cellar_id": "2342"
                    }
                ],
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            },
            "sap_json": {
                "id": "204",
                "type": "sap document",
                "next_task": "end",
                "config": {
                    "type_document": "39",
                    "username": "LOGINPLAY",
                    "password": "1234",
                    "site_name": "wildfoods-sap",
                    "WarehouseCode": "BODECOMC",
                    "company_db": "TESTWF",
                    "site_url": "https",
                    "access_token_lp": "x"
                }
            }
        }
        expected_ouput = {
            "User": {
                "Password": "1234",
                "UserName": "LOGINPLAY"
            },
            "SN": {
                "CardCode": "C77777777-7C",
                "CardName": "María Paz",
                "CardType": "cCustomer",
                "GroupCode": 100,
                "FederalTaxID": "77777777-7",
                "EmailAddress": "mperrazuriz@aptus.org",
                "CardForeignName": "Shopify",
                "ShipToDefault": "DESPACHO",
                "BilltoDefault": "FACTURACION",
                "U_SEI_GNRP": "GOBIERNO",
                "DebitorAccount": "110401001",
                "U_Tipo": "N",
                "Currency": "CLP",
                "BPAddresses": [
                    {
                        "AddressName": "DESPACHO",
                        "Street":
                            "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                        "City": "chile",
                        "County": "Vitacura",
                        "Country": "CL",
                        "State": "1",
                        "TaxCode": "IVA",
                        "AddressType": "bo_ShipTo"
                    },
                    {
                        "AddressName": "FACTURACION",
                        "Street":
                            "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                        "City": "chile",
                        "County": "Vitacura",
                        "Country": "CL",
                        "State": "1",
                        "TaxCode": "IVA",
                        "AddressType": "bo_BillTo"
                    }
                ],
                "ContactEmployees": [
                    {
                        "Name": "María Paz Errazuriz",
                        "Phone1": "992825655",
                        "E_Mail": "mperrazuriz@aptus.org",
                        "FirstName": "María Paz",
                        "MiddleName": "null",
                        "LastName": "Errazuriz"
                    }
                ]
            },
            "Order": {
                "U_SEI_IDPS": "wildfoods-sap-#59942",
                "DocDate": "2022-02-14T09:12:44.716972",
                "DocDueDate": "2022-02-14T09:12:44.716972",
                "TaxDate": "2022-02-14T09:12:44.716972",
                "CardCode": "C77777777-7",
                "DocCurrency": "CLP",
                "DocRate": 1,
                "SalesPersonCode": 4,
                "ContactPersonCode": "null",
                "U_SEI_MAILCLIENTE": "mperrazuriz@aptus.org",
                "Indicator": "39",
                "FederalTaxID": "77777777-7",
                "U_SEI_FOREF": "#59942",
                "U_SEI_FEREF": "2022-02-14T09:12:44.716972",
                "U_SEI_INREF": 801,
                "U_SEI_CANAL": "CAN03",
                "DocumentLines": [
                    {
                        "ItemCode": "30402",
                        "TaxCode": "IVA",
                        "Quantity": 6.0,
                        "UnitPrice": 4193.277311,
                        "WarehouseCode": "BODECOMC",
                        "DiscountPercent": 0,
                        "BatchNumbers": [
                            {
                                "BatchNumber": "shopify",
                                "Quantity": 6.0
                            }
                        ]
                    },
                    {
                        "ItemCode": "envio",
                        "TaxCode": "IVA",
                        "Quantity": 1,
                        "WarehouseCode": "BODECOMC",
                        "UnitPrice": 2512.61
                    }
                ]
            },
            "Pago": {
                "CounterReference": "200",
                "CreditCard": 3,
                "CreditCardNumber": "6789",
                "CardValidUntil": "2022-12-31",
                "VoucherNum": "200",
                "ConfirmationNum": "400",
                "NumOfPayments": 1
            }
            }
        send_data = ConvertSapDocument(input_data)
        result = send_data.join_json_sap()
        assert result == expected_ouput

    def test_get_products_batch_wildfood_success(self):
        input_data = {
            "order": {
                "id": 3825128,
                "date": "2022-02-14T09:12:44.716972",
                "type": 1,
                "subtotal": 29940.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 32930.0,
                "items_quantity": "None",
                "products_quantity": "None",
                "billing_id": 72542921,
                "shipping_id": 72542921,
                "payment_type": "shopify",
                "source": "",
                "voucher": "",
                "tracking_code": "",
                "provider_id": "None",
                "site_id": "None",
                "extra_info": {
                    "name": "#59942",
                    "bill_comment": "Pedido Shopify: #59942",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 24164719591620,
                    "processing_method": "offsite",
                    "currency": "CLP"
                },
                "name": "",
                "reference_code": "4356494033092",
                "deleted": False,
                "adjustment": -0.0,
                "origin": "shopify",
                "url_document": "",
                "site_name": "wildfoods",
                "status": "despachado",
                "discount_code": "",
                "customer_id": 12862185,
                "cellar_id": 2342,
                "status_counter": 0,
                "multicellar": False,
                "tags": "low-risk, no_superalimento, oficina, Online Store",
                "payments": [
                    {
                        "name": "PAGO_FACIL",
                        "amount": 32930.0
                    }
                ],
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "combination": "",
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "taxable": True,
                        "cellar_id": "2342"
                    }
                ],
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            },
            "sap_json": {
                "id": "204",
                "type": "sap document",
                "next_task": "end",
                "config": {
                    "type_document": "39",
                    "username": "LOGINPLAY",
                    "password": "1234",
                    "site_name": "wildfoods-sap",
                    "WarehouseCode": "BODECOMC",
                    "company_db": "TESTWF",
                    "site_url": "https",
                    "access_token_lp": "x"
                }
            }
            }
        expected_ouput = [
            {
                "ItemCode": "30402",
                "TaxCode": "IVA",
                "Quantity": 6.0,
                "UnitPrice": 4193.277311,
                "WarehouseCode": "BODECOMC",
                "DiscountPercent": 0,
                "BatchNumbers": [
                    {
                        "BatchNumber": "shopify",
                        "Quantity": 6.0
                    }
                ]
            },
            {
                "ItemCode": "envio",
                "TaxCode": "IVA",
                "Quantity": 1,
                "WarehouseCode": "BODECOMC",
                "UnitPrice": 2512.61
            }
        ]
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_products_batch()
        assert result == expected_ouput

    def test_get_products_batch_other_success(self):
        # solo para cliente de wildfoods se le debe agregar el BatchNumbers
        input_data = {
            "order": {
                "id": 3825128,
                "date": "2022-02-14T09:12:44.716972",
                "type": 1,
                "subtotal": 29940.0,
                "shipping": {
                    "cost": 2990.0,
                    "address_line_1":
                        "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "address_line_2": "",
                    "city": "Santiago",
                    "town": "Vitacura",
                    "country": "chile"
                },
                "tax": 0.0,
                "total": 32930.0,
                "items_quantity": "None",
                "products_quantity": "None",
                "billing_id": 72542921,
                "shipping_id": 72542921,
                "payment_type": "shopify",
                "source": "",
                "voucher": "",
                "tracking_code": "",
                "provider_id": "None",
                "site_id": "None",
                "extra_info": {
                    "name": "#59942",
                    "bill_comment": "Pedido Shopify: #59942",
                    "payment_gateway": [
                        "pago_fácil"
                    ],
                    "checkout_id": 24164719591620,
                    "processing_method": "offsite",
                    "currency": "CLP"
                },
                "name": "",
                "reference_code": "4356494033092",
                "deleted": False,
                "adjustment": -0.0,
                "origin": "shopify",
                "url_document": "",
                "site_name": "lamawild-sap",
                "status": "despachado",
                "discount_code": "",
                "customer_id": 12862185,
                "cellar_id": 2342,
                "status_counter": 0,
                "multicellar": False,
                "tags": "low-risk, no_superalimento, oficina, Online Store",
                "payments": [
                    {
                        "name": "PAGO_FACIL",
                        "amount": 32930.0
                    }
                ],
                "products": [
                    {
                        "id": 7128942,
                        "quantity": 6.0,
                        "subtotal": 29940.0,
                        "order_id": 3825128,
                        "size": "",
                        "price": 4990.0,
                        "combination": "",
                        "sku": "30402",
                        "name": "Wild Fit Coco 5 Unidades",
                        "discount": 0.0,
                        "barcode": "",
                        "taxable": True,
                        "cellar_id": "2342"
                    }
                ],
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "El Arcángel 4950 Dpto 703 Vitacura Santiago",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            },
            "sap_json": {
                "id": "204",
                "type": "sap document",
                "next_task": "end",
                "config": {
                    "type_document": "39",
                    "username": "LOGINPLAY",
                    "password": "1234",
                    "site_name": "lamawild-sap",
                    "WarehouseCode": "BODECOMC",
                    "company_db": "TESTWF",
                    "site_url": "https",
                    "access_token_lp": "x"
                }
            }
            }
        expected_ouput = [
            {
                "ItemCode": "30402",
                "TaxCode": "IVA",
                "Quantity": 6.0,
                "UnitPrice": 4193.277311,
                "WarehouseCode": "BODECOMC",
                "DiscountPercent": 0,
            },
            {
                "ItemCode": "envio",
                "TaxCode": "IVA",
                "Quantity": 1,
                "WarehouseCode": "BODECOMC",
                "UnitPrice": 2512.61
            }
        ]
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_products_batch()
        assert result == expected_ouput

    def test_get_sn_long_maximum_100_in_street(self):
        input_data = {
            "order": {
                "id": 3825128,
                "extra_info": {
                    "currency": "CLP"
                },
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "llllllllllllllllllllllllllllllllllllllllllllll"
                    "lllllllllllllllllllllllllllllllllllllllllllllllllll"
                    "llo",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "additional_info": "",
                    "town": "",
                    "country": "chile",
                    "rut": "",
                    "type": "persona",
                    "city": "Vitacura",
                    "region": "Santiago",
                    "customer_id": 12862185,
                    "last_name": "Errazuriz"
                }
            }
        }
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_sn()
        expected_ouput = {
            "CardCode": "C77777777-7C",
            "CardName": "María Paz",
            "CardType": "cCustomer",
            "GroupCode": 100,
            "FederalTaxID": "77777777-7",
            "EmailAddress": "mperrazuriz@aptus.org",
            "CardForeignName": "Shopify",
            "ShipToDefault": "DESPACHO",
            "BilltoDefault": "FACTURACION",
            "U_SEI_GNRP": "GOBIERNO",
            "DebitorAccount": "110401001",
            "U_Tipo": "N",
            "Currency": "CLP",
            "BPAddresses": [
                {
                    "AddressName": "DESPACHO",
                    "Street": "llllllllllllllllllllllllllllllllllllllllllllll"
                        "lllllllllllllllllllllllllllllllllllllllllllllllllll"
                        "ll",
                    "City": "chile",
                    "County": "Vitacura",
                    "Country": "CL",
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_ShipTo"
                },
                {
                    "AddressName": "FACTURACION",
                    "Street": "llllllllllllllllllllllllllllllllllllllllllllll"
                    "lllllllllllllllllllllllllllllllllllllllllllllllllll"
                    "ll",
                    "City": "chile",
                    "County": "Vitacura",
                    "Country": "CL",
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_BillTo"
                }
            ],
            "ContactEmployees": [
                {
                    "Name": "María Paz Errazuriz",
                    "Phone1": "992825655",
                    "E_Mail": "mperrazuriz@aptus.org",
                    "FirstName": "María Paz",
                    "MiddleName": "null",
                    "LastName": "Errazuriz"
                }
            ]
        }

        assert result == expected_ouput

    def test_get_sn_address_null_or_empty(self):
        input_data = {
            "order": {
                "id": 3825128,
                "extra_info": {
                    "currency": "CLP"
                },
                "customer": {
                    "id": 72542921,
                    "name": "María Paz",
                    "email": "mperrazuriz@aptus.org",
                    "address": "",
                    "telephone": "992825655",
                    "zip_code": "CL",
                    "country": "",
                    "rut": "",
                    "city": "",
                    "region": "",
                    "last_name": "Errazuriz"
                }
            }
        }
        send_data = ConvertSapDocument(input_data)
        result = send_data.get_sn()
        expected_ouput = {
            "CardCode": "C77777777-7C",
            "CardName": "María Paz",
            "CardType": "cCustomer",
            "GroupCode": 100,
            "FederalTaxID": "77777777-7",
            "EmailAddress": "mperrazuriz@aptus.org",
            "CardForeignName": "Shopify",
            "ShipToDefault": "DESPACHO",
            "BilltoDefault": "FACTURACION",
            "U_SEI_GNRP": "GOBIERNO",
            "DebitorAccount": "110401001",
            "U_Tipo": "N",
            "Currency": "CLP",
            "BPAddresses": [
                {
                    "AddressName": "DESPACHO",
                    "Street": "Sin direccion",
                    "City": "Sin direccion",
                    "County": "Sin direccion",
                    "Country": "CL",
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_ShipTo"
                },
                {
                    "AddressName": "FACTURACION",
                    "Street": "Sin direccion",
                    "City": "Sin direccion",
                    "County": "Sin direccion",
                    "Country": "CL",
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_BillTo"
                }
            ],
            "ContactEmployees": [
                {
                    "Name": "María Paz Errazuriz",
                    "Phone1": "992825655",
                    "E_Mail": "mperrazuriz@aptus.org",
                    "FirstName": "María Paz",
                    "MiddleName": "null",
                    "LastName": "Errazuriz"
                }
            ]
        }

        assert result == expected_ouput

    @patch("app.convert_sap_document.ConvertSapDocument.get_products")
    @patch("app.convert_sap_document.ConvertSapDocument.send_sap")
    @patch("app.convert_sap_document.requests.post")
    def test_validate_article_in_sap_product_success(
            self, mock_request_post, mock_send_sap, mock_get_products):
        input_data = {
            "sap_json": {
                "config": {
                    "company_db": "company-test",
                    "password": "password-test",
                    "username": "username-test",
                    "access_token_lp": "access_token_lp-test"
                }
            },
            "order": {
                "id": "order-id"
            }
        }
        product = [{
            "ItemCode": "xx"
        }]
        return_send_sap = {"status": "success"}
        expected_ouput = {"status": "success"}
        return_requests_post = [{"itemcode": "xx", "product": "product"}]

        mock_request_post.return_value.json.return_value = return_requests_post
        mock_send_sap.return_value = return_send_sap
        mock_get_products.return_value = product

        send_data = ConvertSapDocument(input_data)
        result = send_data.validate_article_in_sap()
        assert result == expected_ouput

    @patch("app.convert_sap_document.ConvertSapDocument.get_products")
    @patch("app.convert_sap_document.ConvertSapDocument.send_sap")
    @patch("app.convert_sap_document.requests.post")
    @patch("app.convert_sap_document.requests.put")
    def test_validate_article_in_sap_product_failed(
            self, mock_request_put,
            mock_request_post,
            mock_send_sap,
            mock_get_products):
        input_data = {
            "sap_json": {
                "config": {
                    "company_db": "company-test",
                    "password": "password-test",
                    "username": "username-test",
                    "access_token_lp": "access_token_lp-test"
                }
            },
            "order": {
                "id": "order-id"
            }
        }
        product = [{
            "ItemCode": "xx"
        }]
        return_send_sap = {"status": "success"}
        expected_ouput = {"status": "success"}
        return_requests_post = []
        return_requests_put = {"status": "success"}

        mock_request_post.return_value.json.return_value = return_requests_post
        mock_request_put.return_value.json.return_value = return_requests_put
        mock_send_sap.return_value = return_send_sap
        mock_get_products.return_value = product

        send_data = ConvertSapDocument(input_data)
        result = send_data.validate_article_in_sap()
        assert result == expected_ouput

    @patch("app.convert_sap_document.ConvertSapDocument.join_json_sap")
    @patch("app.convert_sap_document.requests.post")
    def test_send_sap(self, mock_request_post, mock_join_json_sap):
        input_data = {
            "sap_json": {
                "config": {
                    "company_db": "company-test",
                    "password": "password-test",
                    "username": "username-test",
                    "access_token_lp": "access_token_lp-test",
                    "site_url": "site_url-test"
                }
            },
            "order": {
                "id": "order-id"
            }
        }
        return_mock_request_post = {
            "creado": "true",
            "boleta": "url-pdf",
            "folio": "folio-test"}

        return_mock_join_json_sap = {"order": "order_test"}

        expected_ouput = {
            "creado": "true",
            "boleta": "url-pdf",
            "folio": "folio-test"}

        mock_request_post.return_value.json.return_value =\
            return_mock_request_post
        mock_join_json_sap.return_value = return_mock_join_json_sap
        send_data = ConvertSapDocument(input_data)
        result = send_data.send_sap()
        assert result == expected_ouput
