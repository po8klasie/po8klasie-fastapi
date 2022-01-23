from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.api.schools.query_utils import get_schools, get_school
from app.db.db import get_db

schools_router = APIRouter()


class SubfieldMappingSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class SchoolListItemSchema(BaseModel):
    project_id: str
    name: str
    rspo: str
    latitude: float
    longitude: float
    street: str
    building_number: str
    apartment_number: str
    borough: str
    city: str
    facility_type: SubfieldMappingSchema

    class Config:
        orm_mode = True


@schools_router.get("/", response_model=Page[SchoolListItemSchema])
def route_get_schools(project_id: str = None, db: Session = Depends(get_db)):
    return paginate(get_schools(db, project_id))


class SchoolResponseSchema(SchoolListItemSchema):
    email: str
    phone: str
    website: str

    class Config:
        orm_mode = True


@schools_router.get("/{rspo}", response_model=SchoolResponseSchema)
def route_get_school(rspo: str, db: Session = Depends(get_db)):
    return get_school(db, rspo)
