
class ConvertSapDocument():

    def reception_data(self, data: dict):
        json_sap_document = {
            "User":{
                "Password":"Sbo.2021",
                "UserName":"wildbrands\\rhidalgo"
            },
            "SN":{
                "CardCode":"C57909659-4",
                "CardName":"DELIA RIQUELME VERA",
                "CardType":"cCustomer",
                "GroupCode":100,
                "FederalTaxID":"57909659-4",
                "EmailAddress":"null",
                "CardForeignName":"SERVICIO DE SALUD IQUIQUE",
                "ShipToDefault":"DESPACHO",
                "BilltoDefault":"FACTURACION",
                "U_SEI_GNRP":"GOBIERNO",
                "U_Tipo":"N",
                "DebitorAccount":"110401001",
                "Currency":"CLP",
                "BPAddresses":[
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
                "ContactEmployees":[
                    {
                        "Name":"Delia Riquelme",
                        "Phone1":"56-57-2535017",
                        "E_Mail":"juan.toros@redsalud.gob.cl",
                        "FirstName":"Delia",
                        "MiddleName":"null",
                        "LastName":"TORO"
                    }
                ]
            },
            "Order":{
                "U_SEI_IDPS":"1klkl7",
                "DocDate":"2022-01-11",
                "DocDueDate":"2022-01-11",
                "TaxDate":"2022-01-11",
                "CardCode":"C57909659-4",
                "DocCurrency":"CLP",
                "DocRate":1,
                "SalesPersonCode":1,
                "ContactPersonCode":null,
                "ShipToCode":"DESPACHO",
                "Indicator":"39",
                "FederalTaxID":"57909659-4",
                "DiscountPercent":0,
                "U_SEI_FOREF":"19/2021",
                "U_SEI_FEREF":"2021-11-30",
                "U_SEI_INREF":801,
                "DocumentLines":[
                    {
                        "CostingCode":"CC01",
                        "ItemCode":"INAIPSOY02",
                        "TaxCode":"IVA",
                        "Quantity":1,
                        "Price":3500
                    }
                ]
            },
            "Pago":{
                "CreditCard":1,
                "CreditCardNumber":"6789",
                "CardValidUntil":"2021-12-31",
                "VoucherNum":"200",
                "ConfirmationNum":"400",
                "NumOfPayments":1
            }
        }
        return json_sap_document