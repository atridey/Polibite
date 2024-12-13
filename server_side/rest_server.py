from data_interface import *

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(root_path = '/api', redoc_url = None)
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",  # React/Frontend origin
    "http://127.0.0.1:3000"
]

@app.get('/get_dates/')
def return_dates():
    return {'date_list': get_dates()}


@app.get('/get_summary/{ISOSTRING}')
def return_summary(ISOSTRING: str):
    return {'summary': get_summary(ISOSTRING).split('\n')}
