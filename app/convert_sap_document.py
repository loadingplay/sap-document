import requests
from fastapi import HTTPException
import logging
import json
import os


logging.getLogger().setLevel(logging.INFO)

LP_API = os.getenv('LP_API', '')

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


        json_sn = {
            "CardCode": "C77777777-7C",
            "CardName": order["customer"]["name"],
            "CardType": "cCustomer",
            "GroupCode": 100,
            "FederalTaxID": FederalTaxID,
            "EmailAddress": order["customer"]["email"],
            "CardForeignName":"SERVICIO DE SALUD IQUIQUE", # duda
            "ShipToDefault":"DESPACHO", # duda
            "BilltoDefault":"FACTURACION", # duda
            "U_SEI_GNRP": "GOBIERNO",
            "DebitorAccount":"110401001", # Se recomienda no enviar
            "U_Tipo": "N",
            "Currency": order["extra_info"]["currency"],
            "BPAddresses":[
                {
                    "AddressName":"DESPACHO",
                    "Street": order["customer"]["address"],
                    "City": order["customer"]["country"],
                    "County": order["customer"]["city"],
                    "Country": "CL", # Por el momento dejarlo en duro
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType":"bo_ShipTo"
                },
                {
                    "AddressName":"FACTURACION",
                    "Street": order["customer"]["address"],
                    "City": order["customer"]["country"],
                    "County": order["customer"]["city"],
                    "Country": "CL", # Por el momento dejarlo en duro
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType":"bo_BillTo"
                }
            ],
            "ContactEmployees":[ # nodo duda
                {
                    "Name": order["customer"]["name"]+" "+order["customer"]["last_name"],
                    "Phone1": order["customer"]["telephone"],
                    "E_Mail": order["customer"]["email"],
                    "FirstName": order["customer"]["name"],
                    "MiddleName":"null",
                    "LastName": order["customer"]["last_name"],
                }
            ]

        }

        return json_sn

    def get_products(self):

        products = self.__data["order"]["products"]

        if self.__data["order"]["shipping"]:
            products.append({
                "sku": "envio",
                "quantity": 1,
                "price": self.__data["order"]["shipping"]["cost"]
                })
        json_product= []

        for item in products:
            json_product.append({
                "ItemCode": item["sku"],
                "TaxCode":"IVA",
                "Quantity": item["quantity"],
                "Price": item["price"]
            })
        return json_product

    def get_order(self):
        order = self.__data["order"]
        config = self.__data["sap_json"]["config"]
        FederalTaxID = self.__data["order"]["customer"]["rut"]

        if FederalTaxID == "":
            FederalTaxID = "77777777-7C"

        json_order = {
            "U_SEI_IDPS": config["site_name"] +"-"+ order["extra_info"]["name"],
            "DocDate": order["date"],
            "DocDueDate": order["date"],
            "TaxDate": order["date"],
            "CardCode": "C"+FederalTaxID,
            "DocCurrency": order["extra_info"]["currency"],
            "DocRate":1,
            "SalesPersonCode":1, # duda
            "ContactPersonCode":"null", # duda
            "ShipToCode":"DESPACHO", # duda
            "Indicator": config["type_document"],
            "FederalTaxID": "61606100-3",
            "DiscountPercent": order["adjustment"],
            "U_SEI_FOREF": str(order["extra_info"]["name"]),
            "U_SEI_FEREF": "2021-05-18",
            "U_SEI_INREF":801,
            "DocumentLines": self.get_products()

        }
        return json_order

    def get_pago(self):

        json_pago = {
            "CreditCard":1,
            "CreditCardNumber":"6789",
            "CardValidUntil":"2022-12-31",
            "VoucherNum":"200",
            "ConfirmationNum":"400",
            "NumOfPayments":1
        }
        return json_pago

    def join_json_sap(self):

        json_sap_document = {
            "User": self.get_user(),
            "SN":self.get_sn(),
            "Order": self.get_order(),
            "Pago": self.get_pago()
        }

        return json_sap_document

    def validate_article_in_sap(self):
        user = self.__data["sap_json"]["config"]
        order = self.__data["order"]
        credentials = {
            "CompanyDB": "DESARROLLO2",
            "Password": user["password"],
            "UserName": user["username"],
            "Language": "23"
        }
        products = self.get_products()
        product_error = []
        for product in products:
            article = product["ItemCode"]
            response = requests.post(
                f"https://sbo-wildbrands.cloudseidor.com:4300/Wildbrands/Integracion/ObtenerItems.xsjs?$select=ItemCode,ItemName,ForeignName&$filter=ItemCode eq '{article}'",
                json=credentials
            )
            if len(response.json()) == 0:
                product_error.append(article)

        product_not_found = {
            "product_not_found": product_error
        }
        if len(product_error) == 0:
            return self.send_sap()
        else:
            order_id = order["id"]
            access_token = user["access_token_lp"]
            error = json.dumps(product_error)
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

        try:
            response = requests.post(
                "https://sbo-wildbrands.cloudseidor.com:4300/Wildbrands/Integracion/App.xsjs",
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
