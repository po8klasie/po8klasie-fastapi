from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.api.api_router import api_router
from app.config import settings
from app.sentry import setup_sentry

setup_sentry()

app = FastAPI(title="po8klasie-fastapi")

app.include_router(api_router, prefix="/api")

add_pagination(app)


if settings.environment == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def read_root():
    return {"hello": "world"}
