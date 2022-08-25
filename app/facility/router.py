from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.facility.schemas import FacilityResponseSchema, FacilityListItemSchema
from app.router_utils import MaxPaginationLimitPage
from db.db import get_db
from app.facility.models import get_facility, get_facilities, Facility

facility_router = APIRouter()


@facility_router.get("/", response_model=MaxPaginationLimitPage[FacilityListItemSchema])
def route_get_schools(
    project_id: Optional[str] = None,
    query: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    facilities = get_facilities(db, project_id)

    if query:
        facilities = facilities.filter(
            func.lower(Facility.name).contains(query.lower(), autoescape=True)
        )

    if is_public is not None:
        facilities = facilities.filter(Facility.is_public == is_public)

    return paginate(facilities)


@facility_router.get("/{rspo}", response_model=FacilityResponseSchema)
def route_get_facility(rspo: str, db: Session = Depends(get_db)):
    return get_facility(db, rspo)
