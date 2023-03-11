from typing import Optional, List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.search.map_features import bbox_str_to_polygon_wkt
from po8klasie_fastapi.app.institution.models import (
    SecondarySchoolInstitution,
    query_secondary_school_institutions,
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


def filter_by_points_threshold(institutions, points_threshold: [int, int]):
    if len(points_threshold) != 2:
        return institutions

    threshold_min, threshold_max = sorted(points_threshold)

    if threshold_min < 0 or threshold_min > 200:
        return institutions

    return institutions.filter(
        and_(
            SecondarySchoolInstitution.points_stats_min >= threshold_min,
            SecondarySchoolInstitution.points_stats_min <= threshold_max,
        )
    )


def filter_institutions(
    db: Session,
    project_id: Optional[str] = None,
    query: Optional[str] = None,
    languages: Optional[List[str]] = None,
    points_threshold: Optional[List[int]] = None,
    is_public: Optional[bool] = None,
    rspo_institution_type: Optional[List[str]] = None,
    bbox: Optional[str] = None,
):
    institutions = query_secondary_school_institutions(
        db, search_router_secondary_school_entities
    )

    if project_id:
        institutions = filter_by_project_id(institutions, project_id)

    if query:
        institutions = filter_by_query(institutions, query)

        return institutions

    if languages:
        institutions = filter_by_languages(institutions, languages)

    if points_threshold:
        institutions = filter_by_points_threshold(institutions, points_threshold)

    if is_public is not None:
        institutions = institutions.filter(RspoInstitution.is_public == is_public)

    if rspo_institution_type:
        institutions = institutions.filter(
            RspoInstitution.rspo_institution_type.in_(rspo_institution_type)
        )

    if bbox:
        bbox_polygon_wkt = bbox_str_to_polygon_wkt(bbox)
        institutions = institutions.filter(
            SecondarySchoolInstitution.geometry.ST_Within(bbox_polygon_wkt)
        )

    return institutions
