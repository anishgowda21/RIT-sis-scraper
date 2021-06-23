import json
from typing import Optional
from fastapi import FastAPI
from scrapper import get_data
app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "word"}


@app.get("/sis/")
def get_item(usn: str, dob: str):
    return (get_data(usn, dob))
