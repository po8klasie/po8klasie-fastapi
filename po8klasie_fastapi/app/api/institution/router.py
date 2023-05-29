from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, contains_eager

from po8klasie_fastapi.app.api.institution.schemas import InstitutionDetailsSchema
from po8klasie_fastapi.app.api.schemas import InstitutionOverviewSchema
from po8klasie_fastapi.app.institution.models import (
    SecondarySchoolInstitution,
    query_institutions,
)
from po8klasie_fastapi.app.rankings.zwzt.models import ZwzTRankingEntry

from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution
from po8klasie_fastapi.db.db import get_db

school_router = APIRouter()


@school_router.get("/", response_model=list[InstitutionOverviewSchema])
def route_get_schools(db: Session = Depends(get_db)):
    return query_institutions(db).all()


@school_router.get("/multiple", response_model=list[InstitutionOverviewSchema])
def route_multiple_institutions_overview(
    rspo: List[str] = Query(default=[]), db: Session = Depends(get_db)
):
    if len(rspo) == 0:
        raise HTTPException(status_code=422, detail="No rspos provided")

    try:
        institutions = (
            query_institutions(db)
            .filter(SecondarySchoolInstitution.rspo.in_(rspo))
            .all()
        )

        for institution in institutions:
            yield InstitutionOverviewSchema.parse_institution(institution)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="No schools found")


@school_router.get("/{rspo}", response_model=InstitutionDetailsSchema)
def route_get_single_school(rspo: str, db: Session = Depends(get_db)):
    try:
        institution = (
            query_institutions(db, with_public_transport=True)
            .filter(RspoInstitution.rspo == rspo)
            .one()
        )

        return InstitutionDetailsSchema.parse_institution(institution)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No school found")
