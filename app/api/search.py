from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.schemas.search_schemas import SearchListItemSchema
from app.institution.models import (
    query_secondary_school_institutions,
    SecondarySchoolInstitution,
)
from app.lib.router_utils import MaxPaginationLimitPage
from app.rspo_institution.models import RspoInstitution
from db.models import Institution
from db.db import get_db

search_router = APIRouter()

search_router_secondary_school_entities = [
    SecondarySchoolInstitution.project_id,
    SecondarySchoolInstitution.rspo,
    SecondarySchoolInstitution.institution_type_generalized,
    RspoInstitution.name,
    RspoInstitution.street,
    RspoInstitution.building_number,
    RspoInstitution.apartment_number,
    RspoInstitution.city,
    RspoInstitution.is_public,
    RspoInstitution.latitude,
    RspoInstitution.longitude,
    RspoInstitution.borough,
    RspoInstitution.city,
]


@search_router.get("/", response_model=MaxPaginationLimitPage[SearchListItemSchema])
def search_route(
    project_id: Optional[str] = None,
    query: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    institutions = query_secondary_school_institutions(
        db, search_router_secondary_school_entities
    )

    if project_id:
        institutions = institutions.filter(
            SecondarySchoolInstitution.project_id == project_id
        )

    if query:
        institutions = institutions.filter(
            func.lower(Institution.name).contains(query.lower(), autoescape=True)
        )

    if is_public is not None:
        institutions = institutions.filter(RspoInstitution.is_public == is_public)

    return paginate(institutions.all())
