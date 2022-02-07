import json
from typing import Optional
from fastapi import FastAPI
from SIS import get_sis_data
app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "word"}


@app.get("/sis/")
def get_item(usn: str, dob: str, firstyear: Optional[bool] = None):
    if firstyear:
        return get_sis_data(usn, dob, firstyear)
    return get_sis_data(usn, dob)
