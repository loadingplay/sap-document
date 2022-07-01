import requests
import json
from utils.constants import URL_LOGIN, URL_INVOICES

class sap_creditnote():
    def __init__(self, data) -> None:
        self.__data = data

    def get_linenum():
        s = requests.Session()

        #Ver que hacer con los headers y el CompanyDB, ya que son distintos a los que actualmente tenemos
        s.post(
            URL_LOGIN,
            headers={
            "CompanyDB": "SBOWILDFOODS",
            "Password": "User1234",
            "UserName": "LOGINPLAY"
            },
        )

        #DocEntry debe ir entre parentesis
        DocEntry = 59586
        response = s.get(
            URL_INVOICES+f"({DocEntry})")

        #Aqui nos ahorramos todo el json y solo nos quedamos con la data que nos interesa
        linenum = []
        document_lines = response.json()["DocumentLines"]
        for line in document_lines:
            linenum.append(line["LineNum"])
        linenum_str = json.dumps(linenum)
        print(linenum_str)
        return linenum_str
    

    def ndc():
        linenum = sap_creditnote.get_linenum()
        #La data de DocumentLines se debe repetir tantas veces como datos tenga linenum
        json_ndc = {
            "CardCode": "V50000",
            "DocumentLines": [
                {
                    "BaseEntry": "59586", #DocEntry extra_info
                    "BaseLine": "0", #LineNum
                    "BaseType": "13", #Siempre es 13
                },
                {
                    "BaseEntry": "59586", #DocEntry extra_info
                    "BaseLine": "1", #LineNum
                    "BaseType": "13", #Siempre es 13
                }
            ]
        }
        

