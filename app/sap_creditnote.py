import requests
from fastapi import HTTPException
from app.utils.constants import URL_LOGIN, URL_INVOICES
import logging


class SapCreditNote():
    def __init__(self, data) -> None:
        self.__data = data

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
            linenum.append(line["LineNum"])
        return linenum

    def generate_document_lines(self):
        linenum = self.get_linenum()
        DocEntry = self.__data["order"]["extra_info"]["boleta_sap"]["DocEntry"]
        document_line = []
        for item in linenum:
            document_line.append({
                "BaseEntry": str(DocEntry),
                "BaseLine": str(item),
                "BaseType": "13"
            })
        return document_line

    def build_credit_note(self):
        FederalTaxID = self.__data["order"]["customer"]["rut"]
        if FederalTaxID == "":
            FederalTaxID = "77777777-7"
        if "-" not in FederalTaxID:
            rut = FederalTaxID[:-1]
            digito_verificador = FederalTaxID[-1]
            FederalTaxID = rut + "-" + digito_verificador
        # La data de DocumentLines se debe repetir
        # tantas veces como datos tenga linenum
        json_ndc = {
            "CardCode": "C"+FederalTaxID,
            "DocumentLines": self.generate_document_lines()
        }
        print(json_ndc)
        return json_ndc

    def send_credit_note(self):
        # url = self.__data["sap_json"]["config"]["site_url"]
        url = "https:www.test.com"
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
