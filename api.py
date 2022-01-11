import logging
from fastapi import FastAPI


api = FastAPI()


@api.post("/v1/reception")
def post_sap(data: dict):

    return data

