from data_interface import *

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def greet():
    return {'wsp': 'how u doin', 'politics?': 'bite sized'}

@app.get('/get_dates/')
def return_dates():
    return {'date_list': get_dates()}


@app.get('/get_summary/{ISOSTRING}')
def return_summary(ISOSTRING: str):
    return {'summary': get_summary(ISOSTRING)}