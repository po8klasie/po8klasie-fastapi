from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Required
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.search.filtering import (
    FiltersQuery,
    filter_by_project_id,
    filter_by_query,
    filter_institutions,
    query_institutions,
)
from po8klasie_fastapi.app.api.search.map_features.router import (
    search_map_features_router,
)
from po8klasie_fastapi.app.api.search.ordering import order_institutions
from po8klasie_fastapi.app.api.search.schemas import (
    RspoInstitutionSchema,
    SecondarySchoolInstitutionSchema,
)
from po8klasie_fastapi.app.institution.models import (
    SecondarySchoolInstitution,
    query_secondary_school_institutions,
)
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution
from po8klasie_fastapi.db.db import get_db

search_router = APIRouter()

search_router.include_router(search_map_features_router, prefix="/map_features")


@search_router.get("/autocomplete")
def route_search_autocomplete(
    query: str = Query(default=...),
    project_id: str = Query(default=...),
    db: Session = Depends(get_db),
):
    institutions = query_secondary_school_institutions(
        db,
        [
            SecondarySchoolInstitution.rspo,
            SecondarySchoolInstitution.project_id,
            RspoInstitution.name,
        ],
    )

    institutions = filter_by_query(institutions, query)
    institutions = filter_by_project_id(institutions, project_id)

    return institutions.limit(5).all()


@search_router.get("/institution/{rspo}")
def route_search_single_institution(rspo=Required, db: Session = Depends(get_db)):
    try:
        institution = (
            query_institutions(db, with_public_transport=False)
            .filter(RspoInstitution.rspo == rspo)
            .one()
        )

        return {
            **RspoInstitutionSchema.from_orm(institution.rspo_institution).dict(),
            **SecondarySchoolInstitutionSchema.from_orm(institution).dict(),
            "classes": institution.classes,
        }

    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail={"success": False, "message": "Institution not found"},
        )


@search_router.get("/institution")
def route_search_institutions(
    filters_query: Annotated[FiltersQuery, Depends(FiltersQuery)],
    db: Session = Depends(get_db),
):
    institutions = filter_institutions(db, filters_query.model)
    institutions = order_institutions(institutions)

    for institution in institutions:
        yield {
            **RspoInstitutionSchema.from_orm(institution.rspo_institution).dict(),
            **SecondarySchoolInstitutionSchema.from_orm(institution).dict(),
            "classes": institution.classes,
        }
