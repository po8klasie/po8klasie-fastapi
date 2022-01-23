from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.api import api_router

app = FastAPI(title="po8klasie-fastapi")

app.include_router(api_router, prefix="/api")

add_pagination(app)

@app.get("/")
def read_root():
    return {"hello": "world"}
