import requests
from fastapi import HTTPException
from app.utils.constants import URL_LOGIN, URL_INVOICES
import logging


class SapCreditNote():
    def __init__(self, data) -> None:
        self.__data = data

    def get_user(self):
        user = self.__data["sap_json"]["config"]
        json_user = {
            "Password": user["password"],
            "UserName": user["username"]
        }

        return json_user

    def get_linenum(self):
        s = requests.Session()
        credentials = self.__data["sap_json"]["config"]
        order = self.__data["order"]["extra_info"]

        # Ver que hacer con los headers y el CompanyDB,
        # ya que son distintos a los que actualmente tenemos
        s.post(
            URL_LOGIN,
            headers={
                "CompanyDB": credentials["company_db"],
                "Password": credentials["password"],
                "UserName": credentials["username"]
            },
        )
        # dejare obtencion de cookies por si llegamos a necesitarlas
        # ya que lo solicitaba la documentacion
        cookies_login = s.cookies.get_dict()
        print(cookies_login)

        # DocEntry debe ir entre parentesis
        DocEntry = order["boleta_sap"]["DocEntry"]
        response = s.get(
            URL_INVOICES+f"({DocEntry})")

        # Aqui nos ahorramos todo el json y
        # solo nos quedamos con la data que nos interesa
        linenum = []
        document_lines = response.json()["DocumentLines"]
        for line in document_lines:
            linenum.append({
                "lineNum": line["LineNum"],
                "quantity": line["Quantity"]
                })
        return linenum

    def generate_document_lines(self):
        linenum = self.get_linenum()
        DocEntry = self.__data["order"]["extra_info"]["boleta_sap"]["DocEntry"]
        document_line = []
        for item in linenum:
            document_line.append({
                "BaseEntry": str(DocEntry),
                "BaseLine": str(item["lineNum"]),
                "BaseType": "13",
                "BatchNumbers": [
                    {
                        "BatchNumber": "shopify",
                        "Quantity": item["quantity"]
                    }
                ]
            })
        return document_line

    def get_document_lines_batch(self):
        site_name_order = self.__data["order"]["site_name"]
        json_product = self.generate_document_lines()
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
            "CardCode": FederalTaxID+"C",
            "DocCurrency": currency,
            "DocRate": 1,
            "SalesPersonCode": 4,
            "ContactPersonCode": "null",
            "U_SEI_MAILCLIENTE": order["customer"]["email"],
            "FederalTaxID": FederalTaxID,
            "Indicator": config["type_document"],
            "U_SEI_FOREF": str(order["extra_info"]["name"]),
            "U_SEI_FEREF": order["date"],
            "U_SEI_INREF": 33,  # 39 o 33 Dependiente de si es Factura o Boleta
            "U_SEI_CREF": 1,  # 1 Anula documento de referencia - 2 Corrige texto documento de refencia 3 Corrige montos # noqa
            "U_SEI_CANAL": "CAN03",
            "U_SEI_ESTADOPAGO": "Pagado",
            "U_SEI_FEBOSID": "",
            "DocumentLines": self.get_document_lines_batch()
        }
        return json_order

    def build_credit_note(self):
        json_ndc = {
            "User": self.get_user(),
            "Order": self.get_order()
        }
        return json_ndc

    def send_credit_note(self):
        url = self.__data["sap_json"]["config"]["site_url"]
        try:
            response = requests.post(
                url,
                json=self.build_credit_note()
            )
            logging.info("credit note response: " + str(response.json()))
            return response.json()
        except Exception as ex:
            str_error = (
                f"Error method: post endpoint credit note /v1/generate_document"  # noqa
                f"error: {str(ex)}"
            )
            logging.error(str_error, exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Error on post credit note Sap"
            )
