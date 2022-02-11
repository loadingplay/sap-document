import logging

from fastapi import FastAPI
from fastapi import HTTPException

from app.convert_sap_document import ConvertSapDocument
from app.exceptions import JoinJsonSapError

logging.getLogger().setLevel(logging.INFO)
api = FastAPI()


@api.post("/v1/generate_document")
def post_sap(data: dict):
    logging.info(f"Data: {data}")
    json_data = ConvertSapDocument(data) # --> esto es muy poco probable que falle 
    try:
        data_converted = json_data.join_json_sap()
    except JoinJsonSapError as ex:
        logging.error(f"Error on data conversion: {ex}")
        raise HTTPException(
            400,
            "Error on data conversion"
        )

    logging.info(f"Data transformed: {data_converted}")
    request_document = json_data.validate_article_in_sap() # --> alta posibilidad de fallo
    logging.info(f"Data response of sap: {request_document}")
    return request_document

