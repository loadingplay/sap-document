import logging
from fastapi import FastAPI
from app.convert_sap_document import ConvertSapDocument


api = FastAPI()


@api.post("/v1/reception")
def post_sap(data: dict):
    json_data = ConvertSapDocument()
    data_converted = json_data.reception_data(data)
    logging.info(f"Data transformed: {data_converted}")
    return data_converted

