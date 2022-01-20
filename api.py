import logging
from fastapi import FastAPI
from app.convert_sap_document import ConvertSapDocument


api = FastAPI()


@api.post("/v1/generate_document")
def post_sap(data: dict):
    logging.info(f"Data: {data}")
    json_data = ConvertSapDocument(data)
    data_converted = json_data.join_json_sap()
    logging.info(f"Data transformed: {data_converted}")
    request_document = json_data.send_sap()
    return request_document

