from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI(title="po8klasie-fastapi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

add_pagination(app)


@app.get("/")
def read_root():
    return {"hello": "world"}
