from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.api.comparison.comparison_utils import find_intersection, get_comparison_item
from app.api.comparison.schemas import ComparisonInstitutionSchema
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


def group_classes_by_rspo(db, rspos: List[str]):
    classes_by_rspo = {}
    classes = (
        query_current_classes(db)
        .with_entities(
            SecondarySchoolInstitutionClass.extended_subjects,
            SecondarySchoolInstitutionClass.class_name,
            SecondarySchoolInstitutionClass.institution_rspo,
        )
        .filter(SecondarySchoolInstitutionClass.institution_rspo.in_(rspos))
        .all()
    )
    for class_ in classes:
        rspo = class_.institution_rspo
        extended_subjects = "-".join(class_.extended_subjects)
        if rspo in classes_by_rspo and extended_subjects not in classes_by_rspo[rspo]:
            classes_by_rspo[rspo].append(extended_subjects)
        else:
            classes_by_rspo[rspo] = [extended_subjects]
    return classes_by_rspo


@comparison_router.get("/", response_model=List[ComparisonInstitutionSchema])
def route_comparison(
    rspo: List[str] = Query(default=[]), db: Session = Depends(get_db)
):
    if len(rspo) > 5:
        raise HTTPException(
            status_code=422, detail="You can select up to 5 institutions to compare"
        )

    try:
        institutions: List[SecondarySchoolInstitution] = (
            query_secondary_school_institutions(
                db, school_router_secondary_school_entities
            )
            .filter(SecondarySchoolInstitution.rspo.in_(rspo))
            .all()
        )
        rspos = [institution.rspo for institution in institutions]
        classes_by_rspo = group_classes_by_rspo(db, rspos)

        city_intersection = find_intersection(institutions, property_key="city")
        is_public_intersection = find_intersection(
            institutions, property_key="is_public"
        )
        available_languages_intersection = find_intersection(
            institutions, property_key="available_languages"
        )
        classes_intersection = find_intersection(
            institutions, getter_fn=lambda rspo: classes_by_rspo[rspo]
        )

        for institution in institutions:
            yield {
                "name": institution.name,
                "rspo": institution.rspo,
                "comparison": {
                    "is_public": get_comparison_item(
                        institution.is_public, is_public_intersection
                    ),
                    "city": get_comparison_item(institution.city, city_intersection),
                    "available_languages": get_comparison_item(
                        institution.available_languages,
                        available_languages_intersection,
                    ),
                    "classes": get_comparison_item(
                        classes_by_rspo[institution.rspo], classes_intersection
                    ),
                },
            }

    except NoResultFound:
        raise HTTPException(status_code=404, detail="No schools found")
