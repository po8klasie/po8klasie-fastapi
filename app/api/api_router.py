from fastapi import APIRouter

from app.api.school import school_router
from app.api.search import search_router
from app.app_info.router import app_info_router
from app.project.router import project_router

api_router = APIRouter()

routers = {
    "/project": project_router,
    "/app-info": app_info_router,
    "/school": school_router,
    "/search": search_router,
}


for prefix, router in routers.items():
    api_router.include_router(router, prefix=prefix)
