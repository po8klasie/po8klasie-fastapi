from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.institution_classes.models import (
    query_current_classes,
    SecondarySchoolInstitutionClass,
)
from app.api.institution.router import school_router_secondary_school_entities
from db.db import get_db
from app.institution.models import (
    SecondarySchoolInstitution,
    query_secondary_school_institutions,
)

comparison_router = APIRouter()

comparison_router_secondary_school_entities = [*school_router_secondary_school_entities]


@comparison_router.get("/")
def route_comparison(
    rspo: List[str] = Query(default=[]), db: Session = Depends(get_db)
):
    if len(rspo) > 5 or len(rspo) < 0:
        raise HTTPException(
            status_code=422, detail="You need to select up to 5 institutions to compare"
        )

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
