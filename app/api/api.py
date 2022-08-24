from fastapi import APIRouter

from app.api.app_info.router import app_info_router
from app.api.projects.router import projects_router
from app.api.facility.router import facility_router

api_router = APIRouter()

routers = {
    "/facility": facility_router,
    "/projects": projects_router,
    "/app-info": app_info_router,
}


for prefix, router in routers.items():
    api_router.include_router(router, prefix=prefix)
