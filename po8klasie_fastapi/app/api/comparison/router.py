from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.comparison.comparison_utils import (
    compare,
)
from po8klasie_fastapi.app.api.comparison.schemas import ComparisonInstitution
from po8klasie_fastapi.app.institution.models import (
    SecondarySchoolInstitution,
    query_institutions,
)
from po8klasie_fastapi.db.db import get_db

comparison_router = APIRouter()


@comparison_router.get("/", response_model=list[ComparisonInstitution])
def route_comparison(
    rspo: List[str] = Query(default=[]), db: Session = Depends(get_db)
):
    if len(rspo) > 5 or len(rspo) == 0:
        raise HTTPException(
            status_code=422, detail="You can select up to 5 institutions to compare"
        )

    institutions: List[SecondarySchoolInstitution] = (
        query_institutions(db).filter(SecondarySchoolInstitution.rspo.in_(rspo)).all()
    )

    if len(institutions) != len(rspo):
        raise HTTPException(status_code=404, detail="School(s) not found")

    return compare(institutions)
