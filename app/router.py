from fastapi import APIRouter

from app.app_info.router import app_info_router
from app.project.router import project_router
from app.facility.router import facility_router

api_router = APIRouter()

routers = {
    "/facility": facility_router,
    "/project": project_router,
    "/app-info": app_info_router,
}


for prefix, router in routers.items():
    api_router.include_router(router, prefix=prefix)
