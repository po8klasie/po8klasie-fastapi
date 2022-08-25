from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.institution.schemas import InstitutionResponseSchema, InstitutionListItemSchema
from app.lib.router_utils import MaxPaginationLimitPage
from db.db import get_db
from app.institution.models import get_institution, get_institutions, Institution

institution_router = APIRouter()


@institution_router.get(
    "/", response_model=MaxPaginationLimitPage[InstitutionListItemSchema]
)
def route_get_schools(
    project_id: Optional[str] = None,
    query: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    institutions = get_institutions(db, project_id)

    if query:
        institutions = institutions.filter(
            func.lower(Institution.name).contains(query.lower(), autoescape=True)
        )

    if is_public is not None:
        institutions = institutions.filter(Institution.is_public == is_public)

    return paginate(institutions)


@institution_router.get("/{rspo}", response_model=InstitutionResponseSchema)
def route_get_institution(rspo: str, db: Session = Depends(get_db)):
    return get_institution(db, rspo)
