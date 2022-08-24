from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.api.api_utils import CamelCasedModel, MaxPaginationLimitPage
from app.db.db import get_db
from app.models.facility import get_facility, get_facilities, Facility

facility_router = APIRouter()


class FacilityListItemSchema(CamelCasedModel):
    project_id: str
    name: str
    rspo: str
    rspo_facility_type: int
    street: str
    building_number: str
    apartment_number: str
    city: str

    is_public: bool

    latitude: float
    longitude: float

    borough: str
    city: str

    foreign_languages: Optional[List[str]]
    class_profiles: Optional[List[str]]

    class Config:
        orm_mode = True


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


class FacilityResponseSchema(FacilityListItemSchema):
    email: str
    phone: str
    website: str
    postal_code: str


@facility_router.get("/{rspo}", response_model=FacilityResponseSchema)
def route_get_facility(rspo: str, db: Session = Depends(get_db)):
    return get_facility(db, rspo)
