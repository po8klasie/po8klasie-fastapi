from fastapi import APIRouter

from app.api.comparison.router import comparison_router
from app.api.institution.router import school_router
from app.api.search.router import search_router
from app.api.app_info.router import app_info_router
from app.api.project.router import project_router

api_router = APIRouter()

routers = {
    "/project": project_router,
    "/app-info": app_info_router,
    "/school": school_router,
    "/search": search_router,
    "/comparison": comparison_router,
}


for prefix, router in routers.items():
    api_router.include_router(router, prefix=prefix)
