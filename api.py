import logging
from fastapi import FastAPI
from app.convert_sap_document import ConvertSapDocument
from app.sap_creditnote import SapCreditNote
from fastapi import HTTPException
from app.exceptions import JoinJsonSapError


logging.getLogger().setLevel(logging.INFO)
api = FastAPI()


@api.post("/v1/generate_document")
def post_sap(data: dict):
    order_lp = data["order"].get("id", "")
    logging.info(f"order arrived: {order_lp} Data: {data}")
    try:
        json_data = ConvertSapDocument(data)
        data_converted = json_data.join_json_sap()
        request_document = json_data.validate_article_in_sap()
    except JoinJsonSapError as ex:
        logging.error(f"Error on data conversion: {ex}")
        raise HTTPException(
            400,
            "Error on data conversion"
        )

    logging.info(
        f"Data transformed order_id: {order_lp} data: {data_converted}")
    # request_document = json_data.validate_article_in_sap()
    logging.info(
        f"Data response of sap order: {order_lp} response: {request_document}")
    return request_document

@api.post("/v1/generate_document/credit_note")
def post_sap_credit_note(data: dict):
    order_lp = data["order"].get("id", "")
    logging.info(f"order for credit note arrived: {order_lp} Data: {data}")
    try:
        json_data = SapCreditNote(data)
        data_converted = json_data.build_credit_note()
        # enviar JSON de credit note a Sap
        request_document = json_data.send_credit_note()
    except JoinJsonSapError as ex:
        logging.error(f"Error on data conversion credit_note: {ex}")
        raise HTTPException(
            400,
            "Error on data conversion"
        )

    logging.info(
        f"Data transformed credit_note order_id: {order_lp} data: {data_converted}")
    # request_document = json_data.validate_article_in_sap()
    logging.info(
        f"Data response of sap credit_note order: {order_lp} response: {request_document}")
    return request_document
