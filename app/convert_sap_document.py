
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
            "DebitorAccount":"110401001", # duda
            "U_Tipo": "N",
            "Currency": order["extra_info"]["currency"],
            "BPAddresses":[ # nodo duda
                {
                    "AddressName":"DESPACHO",
                    "Street":"TEST1,",
                    "City":"IQUIQUE",
                    "County":"IQUIQUE",
                    "Country":"CL",
                    "State":"1",
                    "TaxCode":"IVA",
                    "AddressType":"bo_ShipTo"
                },
                {
                    "AddressName":"FACTURACION",
                    "Street":"TEST 2,",
                    "City":"IQUIQUE",
                    "County":"IQUIQUE",
                    "Country":"CL",
                    "State":"1",
                    "TaxCode":"IVA",
                    "AddressType":"bo_BillTo"
                }
            ],
            "ContactEmployees":[ # nodo duda
                {
                    "Name":"Delia Riquelme",
                    "Phone1":"56-57-2535017",
                    "E_Mail":"juan.toros@redsalud.gob.cl",
                    "FirstName":"Delia",
                    "MiddleName":"null",
                    "LastName":"TORO"
                }
            ]

        }

        return json_sn

    def get_products(self):
        products = self.__data["order"]["products"]
        json_product= []

        for item in products:
            json_product.append({
                "ItemCode": item["id"],
                "TaxCode":"IVA",
                "Quantity": item["quantity"],
                "Price": item["price"]
            })
        return json_product

    def get_order(self):
        order = self.__data["order"]
        json_order = {
            "U_SEI_IDPS":223, # duda
            "DocDate": order["date"],
            "DocDueDate": order["date"],
            "TaxDate": order["date"],
            "CardCode": "C"+order["customer"]["rut"],
            "DocCurrency": order["extra_info"]["currency"],
            "DocRate":1,
            "SalesPersonCode":1, # duda
            "ContactPersonCode":"null", # duda
            "ShipToCode":"DESPACHO", # duda
            "Indicator":"39",
            "FederalTaxID": order["customer"]["rut"],
            "DiscountPercent": order["adjustment"],
            "U_SEI_FOREF": order["id"],
            "U_SEI_FEREF": order["date"],
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
