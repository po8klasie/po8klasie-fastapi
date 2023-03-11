from fastapi import APIRouter
from pydantic import BaseModel

from po8klasie_fastapi.app.config import settings

app_info_router = APIRouter()


class AppInfoResponseSchema(BaseModel):
    app_version: str


@app_info_router.get("/", response_model=AppInfoResponseSchema)
async def get_app_info():
    return {"app_version": settings.app_version}
