import requests
from fastapi import HTTPException
import logging


logging.getLogger().setLevel(logging.INFO)

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
        config = self.__data["sap_json"]["config"]
        order = self.__data["order"]

        json_sn = {
            "CardCode": "C"+order["customer"]["rut"],
            "CardName": order["customer"]["name"],
            "CardType": "cCustomer",
            "GroupCode": 100,
            "FederalTaxID": order["customer"]["rut"],
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
                    "Street": "calle,",
                    "City": order["customer"]["city"],
                    "County": order["customer"]["country"],
                    "Country": order["customer"]["zip_code"],
                    "State": "1",
                    "TaxCode": "IVA",
                    "AddressType":"bo_ShipTo"
                },
                {
                    "AddressName":"FACTURACION",
                    "Street": "calle,",
                    "City": order["customer"]["city"],
                    "County": order["customer"]["country"],
                    "Country": order["customer"]["zip_code"],
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
        json_product= []

        for item in products:
            json_product.append({
                "CostingCode": "CC01",
                "ItemCode": item["id"],
                "TaxCode":"IVA",
                "Quantity": item["quantity"],
                "Price": item["price"]
            })
        return json_product

    def get_order(self):
        order = self.__data["order"]
        config = self.__data["sap_json"]["config"]
        json_order = {
            "U_SEI_IDPS": 1122, # duda
            "DocDate": order["date"],
            "DocDueDate": order["date"],
            "TaxDate": order["date"],
            "CardCode": "C"+order["customer"]["rut"],
            "DocCurrency": order["extra_info"]["currency"],
            "DocRate":1,
            "SalesPersonCode":1, # duda
            "ContactPersonCode":"null", # duda
            "ShipToCode":"DESPACHO", # duda
            "Indicator": config["type_document"],
            "FederalTaxID": "61606100-3",
            "DiscountPercent": order["adjustment"],
            "U_SEI_FOREF": str(order["id"]),
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

    def send_sap(self):
        # TODO: falta implementar metetodo que mande a sap}
        # mientras tanto hay un mock
        print(self.join_json_sap())
        try:
            response = requests.post(

                "https://sbo-wildbrands.cloudseidor.com:4300/Wildbrands/Integracion/App.xsjs",
                json=self.join_json_sap(),
                verify=False
            )
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
        #return response.json()