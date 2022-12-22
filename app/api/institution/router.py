from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.api.institution.schemas import SingleSchoolResponseSchema
from app.institution_classes.models import (
    query_current_classes,
    SecondarySchoolInstitutionClass,
)
from app.rspo_institution.models import RspoInstitution
from app.api.search.filtering import search_router_secondary_school_entities
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
        institution = (
            query_secondary_school_institutions(
                db, school_router_secondary_school_entities
            )
            .filter_by(rspo=rspo)
            .one()
        )

        classes = (
            query_current_classes(db)
            .with_entities(
                SecondarySchoolInstitutionClass.extended_subjects,
                SecondarySchoolInstitutionClass.class_name,
            )
            .filter(
                SecondarySchoolInstitutionClass.institution_rspo == institution.rspo
            )
            .all()
        )

        return {**dict(institution), "classes": classes}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="No school found")


@school_router.get("/multiple")
def route_comparison(rspo: List[str] = Query(default=[]), db: Session = Depends(get_db)):
    if len(rspo) < 2:
        raise HTTPException(status_code=422, detail="Invalid number of rspos (<2)")

    try:
        institutions = (
            query_secondary_school_institutions(
                db, school_router_secondary_school_entities
            )
            .filter(SecondarySchoolInstitution.rspo.in_(rspo))
            .all()
        )

        for institution in institutions:
            classes = (
                query_current_classes(db)
                .with_entities(
                    SecondarySchoolInstitutionClass.extended_subjects,
                    SecondarySchoolInstitutionClass.class_name,
                )
                .filter(
                    SecondarySchoolInstitutionClass.institution_rspo == institution.rspo
                )
                .all()
            )
            yield {**dict(institution), "classes": classes}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="No schools found")
