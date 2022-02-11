import logging
from fastapi import FastAPI
from app.convert_sap_document import ConvertSapDocument


logging.getLogger().setLevel(logging.INFO)
api = FastAPI()


@api.post("/v1/generate_document")
def post_sap(data: dict):
    order = data["order"]["id"]
    logging.info(f"order arrived: {order} Data: {data}")
    json_data = ConvertSapDocument(data)
    data_converted = json_data.join_json_sap()
    logging.info(f"Data transformed order_id: {order} data: {data_converted}")
    request_document = json_data.validate_article_in_sap()
    logging.info(f"Data response of sap order: {order} response: {request_document}")
    return request_document

