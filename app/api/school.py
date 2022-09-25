from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.api.schemas.school_schemas import SingleSchoolResponseSchema
from app.rspo_institution.models import RspoInstitution
from app.api.search import search_router_secondary_school_entities
from db.db import get_db
from app.institution.models import (
    SecondarySchoolInstitution,
    query_secondary_school_institutions,
)

school_router = APIRouter()

school_router_secondary_school_entities = [
    *search_router_secondary_school_entities,
    RspoInstitution.postal_code,
    RspoInstitution.email,
    RspoInstitution.phone,
    RspoInstitution.website,
    SecondarySchoolInstitution.description,
    SecondarySchoolInstitution.class_profiles,
]


@school_router.get("/", response_model=List[SingleSchoolResponseSchema])
def route_get_schools(db: Session = Depends(get_db)):
    return query_secondary_school_institutions(
        db, school_router_secondary_school_entities
    ).all()


@school_router.get("/{rspo}", response_model=SingleSchoolResponseSchema)
def route_get_single_school(rspo: str, db: Session = Depends(get_db)):
    try:
        return (
            query_secondary_school_institutions(
                db, school_router_secondary_school_entities
            )
            .filter_by(rspo=rspo)
            .one()
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No school found")
