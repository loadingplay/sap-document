import logging
from fastapi import FastAPI
from app.convert_sap_document import ConvertSapDocument
from fastapi import HTTPException
from app.exceptions import JoinJsonSapError


logging.getLogger().setLevel(logging.INFO)
api = FastAPI()


@api.post("/v1/generate_document")
def post_sap(data: dict):
    order_lp = data["order"].get("id", "")
    logging.info(f"order arrived: {order_lp} Data: {data}")
    json_data = ConvertSapDocument(data)
    try:
        data_converted = json_data.join_json_sap()
    except JoinJsonSapError as ex:
        logging.error(f"Error on data conversion: {ex}")
        raise HTTPException(
            400,
            "Error on data conversion"
        )

    logging.info(
        f"Data transformed order_id: {order_lp} data: {data_converted}")
    request_document = json_data.validate_article_in_sap()
    logging.info(
        f"Data response of sap order: {order_lp} response: {request_document}")
    return request_document

