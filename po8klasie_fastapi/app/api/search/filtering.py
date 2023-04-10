import json
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.search.map_features import (
    bbox_regex,
    bbox_str_to_polygon_wkt,
)
from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
)
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution

search_router_secondary_school_entities = [
    SecondarySchoolInstitution.project_id,
    SecondarySchoolInstitution.rspo,
    SecondarySchoolInstitution.points_stats_min,
    SecondarySchoolInstitution.points_stats_max,
    SecondarySchoolInstitution.institution_type_generalized,
    SecondarySchoolInstitution.available_languages,
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
    RspoInstitution.rspo_institution_type,
]


class FiltersQuerySchema(BaseModel):
    project_id: str | None = None
    bbox: str | None = Field(regex=bbox_regex, default=None)
    query: Optional[str]
    is_public: Optional[bool]
    languages: Optional[List[str]]
    points_threshold: Optional[List[int]]
    rspo_institution_type: Optional[List[str]]
    extended_subjects: Optional[List[List[str]]]

    @validator("extended_subjects", pre=True)
    def preprocess_json(cls, raw: str):
        if not raw:
            return None
        return json.loads(raw)


def filter_by_query(institutions, query: str):
    return institutions.filter(
        func.lower(RspoInstitution.name).contains(query.lower(), autoescape=True)
    )


def filter_by_project_id(institutions, project_id: str):
    return institutions.filter(SecondarySchoolInstitution.project_id == project_id)


def filter_by_languages(institutions, languages: List[str]):
    return institutions.filter(
        SecondarySchoolInstitution.available_languages.contains(languages)
    )


def filter_by_is_public(institutions, is_public):
    return institutions.filter(RspoInstitution.is_public == is_public)


def filter_by_rspo_institution_type(institutions, rspo_institution_type):
    return institutions.filter(
        RspoInstitution.rspo_institution_type.in_(rspo_institution_type)
    )


def filter_by_bbox(institutions, bbox):
    bbox_polygon_wkt = bbox_str_to_polygon_wkt(bbox)
    return institutions.filter(
        SecondarySchoolInstitution.geometry.ST_Within(bbox_polygon_wkt)
    )


def filter_by_points_threshold(institutions, points_threshold: [int, int]):
    if len(points_threshold) != 2:
        return institutions

    threshold_min, threshold_max = sorted(points_threshold)

    if threshold_min < 0 or threshold_max > 200:
        return institutions

    return institutions.filter(
        and_(
            SecondarySchoolInstitution.points_stats_min <= threshold_max,
            SecondarySchoolInstitution.points_stats_max >= threshold_min,
        )
    )


def filter_by_extended_subjects(institutions, extended_subjects_list):
    chainable_filters = []

    for extended_subjects_per_class in extended_subjects_list:
        chainable_filters.append(
            SecondarySchoolInstitutionClass.extended_subjects.contains(
                extended_subjects_per_class
            )
        )

    return (
        institutions.join(SecondarySchoolInstitutionClass)
        .filter(SecondarySchoolInstitutionClass.year == 2023)
        .filter(or_(*chainable_filters))
    )


def filter_institutions(db: Session, filters_query: FiltersQuerySchema):
    institutions = db.query(SecondarySchoolInstitution).join(RspoInstitution)

    if filters_query.project_id:
        institutions = filter_by_project_id(institutions, filters_query.project_id)

    if filters_query.query:
        institutions = filter_by_query(institutions, filters_query.query)

    if filters_query.languages:
        institutions = filter_by_languages(institutions, filters_query.languages)

    if filters_query.points_threshold:
        institutions = filter_by_points_threshold(
            institutions, filters_query.points_threshold
        )

    if filters_query.is_public is not None:
        institutions = filter_by_is_public(institutions, filters_query.is_public)

    if filters_query.rspo_institution_type:
        institutions = filter_by_rspo_institution_type(
            institutions, filters_query.rspo_institution_type
        )

    if filters_query.bbox:
        institutions = filter_by_bbox(institutions, filters_query.bbox)

    if filters_query.extended_subjects:
        institutions = filter_by_extended_subjects(
            institutions, filters_query.extended_subjects
        )

    return institutions
