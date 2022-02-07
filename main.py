from typing import Optional
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from SIS import get_sis_data
app = FastAPI()


@app.get("/")
def root():
    response = RedirectResponse(url="https://anishgowda21.github.io/RIT-sis-scraper/")
    return response


@app.get("/sis/")
def get_item(usn: str, dob: str, firstyear: Optional[bool] = None):
    if firstyear:
        return get_sis_data(usn, dob, firstyear)
    return get_sis_data(usn, dob)
