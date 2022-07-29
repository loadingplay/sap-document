import requests
from fastapi import HTTPException
import logging
import json
import os


logging.getLogger().setLevel(logging.INFO)

LP_API = os.getenv('LP_API', '')
# LP_API = "https://apibodegas.ondev.today"


class ConvertSapDocument():
    def __init__(self, data) -> None:
        self.__data = data

    def get_user(self):
        user = self.__data["sap_json"]["config"]
        json_user = {
            "Password": user["password"],
            "UserName": user["username"]
        }

        return json_user

    def get_sn(self):
        order = self.__data["order"]

        FederalTaxID = self.__data["order"]["customer"]["rut"]
        if FederalTaxID == "":
            FederalTaxID = "77777777-7"
        if "-" not in FederalTaxID:
            rut = FederalTaxID[:-1]
            digito_verificador = FederalTaxID[-1]
            FederalTaxID = rut + "-" + digito_verificador

        address = order["customer"]["address"]
        city = order["customer"]["country"]
        street = address[:99]
        if not order["extra_info"].get("currency"):
            currency = "CLP"
        else:
            currency = order["extra_info"]["currency"]

        if street == "":
            street = "Sin direccion"

        if city == "":
            city = "Sin direccion"

        county = order["customer"]["city"]
        if county == "":
            county = "Sin direccion"

        json_sn = {
            "CardCode": "C77777777-7C",
            "CardName": order["customer"]["name"],
            "CardType": "cCustomer",
            "GroupCode": 100,
            "FederalTaxID": FederalTaxID,
            "EmailAddress": order["customer"]["email"],
            "CardForeignName": "Shopify",  # duda
            "ShipToDefault": "DESPACHO",  # duda
            "BilltoDefault": "FACTURACION",  # duda
            "U_SEI_GNRP": "GOBIERNO",
            "DebitorAccount": "110401001",  # Se recomienda no enviar
            "U_Tipo": "N",
            "Currency": currency,
            "BPAddresses": [
                {
                    "AddressName": "DESPACHO",
                    "Street": street,
                    "City": city,
                    "County": county,
                    "Country": "CL",  # Por el momento dejarlo en duro
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_ShipTo"
                },
                {
                    "AddressName": "FACTURACION",
                    "Street": street,
                    "City": city,
                    "County": county,
                    "Country": "CL",  # Por el momento dejarlo en duro
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType": "bo_BillTo"
                }
            ],
            "ContactEmployees": [  # nodo duda
                {
                    "Name": order["customer"]["name"] + " " + \
                    order["customer"]["last_name"],
                    "Phone1": order["customer"]["telephone"],
                    "E_Mail": order["customer"]["email"],
                    "FirstName": order["customer"]["name"],
                    "MiddleName":"null",
                    "LastName": order["customer"]["last_name"],
                }
            ]

        }

        return json_sn

    def get_products_batch(self):
        site_name_order = self.__data["order"]["site_name"]
        json_product = self.get_products()
        batch_number = "BatchNumbers"
        list_product = []

        if site_name_order == "lamawild-sap":
            for item in json_product:

                if batch_number in item:
                    del item[batch_number]
                    list_product.append(item)

                else:
                    list_product.append(item)
            return list_product
        else:
            list_product = json_product
            return list_product

    def get_products(self):
        IVA = 1.19
        products = self.__data["order"]["products"]
        config = self.__data["sap_json"]["config"]
        json_shipping = []

        if self.__data["order"]["shipping"]:
            json_shipping.append({
                "sku": "envio",
                "quantity": 1,
                "price": self.__data["order"]["shipping"]["cost"]
                })
        json_product = []

        for item in products:

            price = round(item["price"] / IVA, 6)
            discount_order_lp = item["discount"]
            unit_discount = 0
            if not discount_order_lp == 0:
                unit_discount = ((discount_order_lp / item["price"]) * 100)

            json_product.append({
                "ItemCode": item["sku"],
                "TaxCode": "IVA",
                "Quantity": item["quantity"],
                "UnitPrice": price,
                "WarehouseCode": config["WarehouseCode"],
                "DiscountPercent": unit_discount,
                "BatchNumbers": [
                    {
                        "BatchNumber": "shopify",
                        "Quantity": item["quantity"]
                    }
                ]
            })

        for item in json_shipping:
            price_shipping = round(item["price"] / IVA, 2)
            json_product.append({
                "ItemCode": item["sku"],
                "TaxCode": "IVA",
                "Quantity": item["quantity"],
                "WarehouseCode": config["WarehouseCode"],
                "UnitPrice": price_shipping
            })
        return json_product

    def get_discount_percent(self):
        order = self.__data["order"]

        subtotal = order["subtotal"]

        adjustment = order["adjustment"]
        discount = (- (100 * adjustment) / subtotal)
        if adjustment == 0:
            discount = 0
            return discount
        discount = round(discount, 5)
        return discount

    def get_order(self):
        order = self.__data["order"]
        config = self.__data["sap_json"]["config"]
        FederalTaxID = self.__data["order"]["customer"]["rut"]
        if FederalTaxID == "":
            FederalTaxID = "77777777-7"
        if "-" not in FederalTaxID:
            rut = FederalTaxID[:-1]
            digito_verificador = FederalTaxID[-1]
            FederalTaxID = rut + "-" + digito_verificador

        if not order["extra_info"].get("currency"):
            currency = "CLP"
        else:
            currency = order["extra_info"]["currency"]

        json_order = {
            "U_SEI_IDPS":
                config["site_name"] + "-" + order["extra_info"]["name"],
            "DocDate": order["date"],
            "DocDueDate": order["date"],
            "TaxDate": order["date"],
            "CardCode": "C"+FederalTaxID,
            "DocCurrency": currency,
            "DocRate": 1,
            "SalesPersonCode": 4,  # duda
            "ContactPersonCode": "null",  # duda
            "U_SEI_MAILCLIENTE": order["customer"]["email"],
            "Indicator": config["type_document"],
            "FederalTaxID": FederalTaxID,
            "U_SEI_FOREF": str(order["extra_info"]["name"]),
            "U_SEI_FEREF": order["date"],
            "U_SEI_INREF": 801,
            "U_SEI_CANAL": "CAN03",
            "U_SEI_ESTADOPAGO": "Pagado",
            "DocumentLines": self.get_products_batch()
        }
        return json_order

    def get_pago(self):

        json_pago = {
            "CounterReference": "200",
            "CreditCard": 3,
            "CreditCardNumber": "6789",
            "CardValidUntil": "2022-12-31",
            "VoucherNum": "200",
            "ConfirmationNum": "400",
            "NumOfPayments": 1
        }
        return json_pago

    def join_json_sap(self):

        json_sap_document = {
            "User": self.get_user(),
            "SN": self.get_sn(),
            "Order": self.get_order(),
            "Pago": self.get_pago()
        }

        return json_sap_document

    def validate_article_in_sap(self):
        user = self.__data["sap_json"]["config"]
        order = self.__data["order"]
        credentials = {
            "CompanyDB": user["company_db"],
            "Password": user["password"],
            "UserName": user["username"],
            "Language": "23"
        }
        products = self.get_products()
        product_error = []
        for product in products:
            article = product["ItemCode"]
            response = requests.post(
                f"https://sbo-wildbrands.cloudseidor.com:4300/Wildbrands/Integracion/ObtenerItems.xsjs?$select=ItemCode,ItemName,ForeignName&$filter=ItemCode eq '{article}'",  # noqa
                json=credentials
            )
            respose_article = response.json()
            if not respose_article:
                product_error.append(article)

        product_not_found = {
            "product_not_found": product_error
        }
        if len(product_error) == 0:
            return self.send_sap()
        else:
            order_id = order["id"]
            access_token = user["access_token_lp"]
            response = requests.put(
                f"{LP_API}/v1/order/{order_id}",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                params={
                    'extra_info': json.dumps(product_not_found)
                }
            )
            return self.send_sap()

    def send_sap(self):
        url = self.__data["sap_json"]["config"]["site_url"]
        try:
            response = requests.post(
                url,
                json=self.join_json_sap()
            )
            logging.info("sap responded to send sap: " + str(response.json()))
            return response.json()
        except Exception as ex:
            str_error = (
                f"Error method: post endpoint /v1/generate_document"
                f"error: {str(ex)}"
            )
            logging.error(str_error, exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Error on post workflows"
            )
