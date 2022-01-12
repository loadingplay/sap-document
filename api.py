import logging
from fastapi import FastAPI
from app.convert_sap_document import ConvertSapDocument


api = FastAPI()


@api.post("/v1/reception")
def post_sap(data: dict):
    logging.info(f"Data: {data}")
    json_data = ConvertSapDocument(data)
    data_converted = json_data.join_json_sap()
    logging.info(f"Data transformed: {data_converted}")
    return data_converted

