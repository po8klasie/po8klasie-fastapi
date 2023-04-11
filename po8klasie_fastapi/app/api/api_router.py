from fastapi import APIRouter

from po8klasie_fastapi.app.api.app_info.router import app_info_router
from po8klasie_fastapi.app.api.comparison.router import comparison_router
from po8klasie_fastapi.app.api.institution.router import school_router
from po8klasie_fastapi.app.api.institution_classes.router import (
    institution_classes_router,
)
from po8klasie_fastapi.app.api.project.router import project_router
from po8klasie_fastapi.app.api.search.router import search_router

api_router = APIRouter()

routers = {
    "/project": project_router,
    "/app-info": app_info_router,
    "/school": school_router,
    "/search": search_router,
    "/comparison": comparison_router,
    "/institution-classes": institution_classes_router,
}


for prefix, router in routers.items():
    api_router.include_router(router, prefix=prefix)
