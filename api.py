import logging
from fastapi import FastAPI



api = FastAPI()


@api.post("/v1/reception")
def mov_in(data: dict):

    return data
