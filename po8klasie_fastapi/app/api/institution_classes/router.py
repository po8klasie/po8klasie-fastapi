from itertools import chain
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func

from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
)
from po8klasie_fastapi.db.db import get_db

institution_classes_router = APIRouter()


def get_distinct_array_values(db, field):
    values = db.query(func.unnest(field)).distinct().all()
    values = filter(lambda s: bool(s), chain(*values))
    return list(values)


@institution_classes_router.get("/extended-subjects", response_model=List[str])
async def get_distinct_extended_subjects(db=Depends(get_db)):
    return get_distinct_array_values(
        db, SecondarySchoolInstitutionClass.extended_subjects
    )


@institution_classes_router.get("/languages", response_model=List[str])
async def get_distinct_languages(db=Depends(get_db)):
    return get_distinct_array_values(
        db, SecondarySchoolInstitutionClass.available_languages
    )
