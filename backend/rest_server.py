from data_interface import *

from typing import Union
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(redoc_url = None)
router = APIRouter(prefix = '/api')

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",  # React/Frontend origin
    "http://127.0.0.1:3000"
]

@router.get('/get_dates/')
def return_dates():
    return {'date_list': get_dates()}


@router.get('/get_summary/{ISOSTRING}')
def return_summary(ISOSTRING: str):
    return {'summary': get_summary(ISOSTRING).split('\n')}

app.include_router(router)
