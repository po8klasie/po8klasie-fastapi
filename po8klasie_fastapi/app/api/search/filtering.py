import json
from json import JSONDecodeError
from typing import List, Optional

import shapely
from fastapi import Query
from pydantic import BaseModel, Field, validator
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery
from sqlalchemy.orm import Session, contains_eager

from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.institution_classes.consts import (
    INSTITUTION_CLASSES_CURRENT_YEAR,
)
from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
)
from po8klasie_fastapi.app.public_transport_info.models import (
    InstitutionPublicTransportStopAssociation,
    PublicTransportRoute,
    PublicTransportStop,
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

classes_base_filters = [
    RspoInstitution.rspo == SecondarySchoolInstitutionClass.institution_rspo,
    SecondarySchoolInstitutionClass.year == INSTITUTION_CLASSES_CURRENT_YEAR,
]


def query_institutions(
    db: Session, with_public_transport: bool = False
) -> SQLAlchemyQuery:
    institutions = db.query(SecondarySchoolInstitution).join(RspoInstitution)

    institutions = (
        institutions.outerjoin(
            SecondarySchoolInstitutionClass, and_(*classes_base_filters)
        )
        .options(contains_eager(SecondarySchoolInstitution.classes))
        .populate_existing()
    )

    if with_public_transport:
        institutions = institutions.outerjoin(
            InstitutionPublicTransportStopAssociation,
            PublicTransportStop,
            PublicTransportRoute,
        )

    return institutions


bbox_regex = r"^\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+$"


def bbox_str_to_polygon_wkt(bbox_str: str) -> str:
    bbox = map(float, bbox_str.split(","))
    polygon = shapely.geometry.box(*bbox, ccw=True)
    return polygon.wkt


class FiltersQuerySchema(BaseModel):
    project_id: str | None = None
    bbox: str | None = Field(default=None)
    query: Optional[str]
    is_public: Optional[bool]
    languages: Optional[List[str]]
    points_threshold: Optional[List[int]]
    rspo_institution_type: Optional[List[int]]
    public_transport_route_type: Optional[List[str]]
    extended_subjects: Optional[list[list[str]]]

    @validator("extended_subjects", pre=True)
    def preprocess_extended_subjects(cls, raw: str):
        if not raw:
            return None
        try:
            return json.loads(raw)
        except JSONDecodeError:
            return None


class FiltersQuery:
    filters_query_dict = {}
    model: FiltersQuerySchema = None

    def __init__(
        self,
        project_id: str | None = None,
        query: str | None = None,
        is_public: bool | None = None,
        languages: List[str] = Query(default=None),
        points_threshold: List[int] = Query(default=None),
        rspo_institution_type: list[int] = Query(default=None),
        public_transport_route_type: list[str] = Query(default=None),
        # XXX(micorix): Have to be Any. Otherwise, query param is not recognized
        extended_subjects: str | None = None,
        bbox: str | None = Query(regex=bbox_regex, default=None),
    ):
        filters_query_dict = {
            "project_id": project_id,
            "query": query,
            "is_public": is_public,
            "languages": languages,
            "points_threshold": points_threshold,
            "rspo_institution_type": rspo_institution_type,
            "public_transport_route_type": public_transport_route_type,
            "extended_subjects": extended_subjects,
            "bbox": bbox,
        }
        self.model = FiltersQuerySchema.parse_obj(filters_query_dict)


def filter_by_query(
    institutions: SQLAlchemyQuery, query: str | None
) -> SQLAlchemyQuery:
    if not query:
        return institutions
    return institutions.filter(
        func.lower(RspoInstitution.name).contains(query.lower(), autoescape=True)
    )


def filter_by_project_id(
    institutions: SQLAlchemyQuery, project_id: str | None
) -> SQLAlchemyQuery:
    if not project_id:
        return institutions
    return institutions.filter(SecondarySchoolInstitution.project_id == project_id)


def filter_by_languages(
    institutions: SQLAlchemyQuery, languages: List[str] | None
) -> SQLAlchemyQuery:
    if not languages:
        return institutions
    return institutions.filter(
        SecondarySchoolInstitution.available_languages.contains(languages)
    )


def filter_by_is_public(
    institutions: SQLAlchemyQuery, is_public: bool | None
) -> SQLAlchemyQuery:
    if is_public is None:
        return institutions
    return institutions.filter(RspoInstitution.is_public == is_public)


def filter_by_rspo_institution_type(
    institutions: SQLAlchemyQuery, rspo_institution_type: list[int] | None
):
    if not rspo_institution_type:
        return institutions
    return institutions.filter(
        RspoInstitution.rspo_institution_type.in_(rspo_institution_type)
    )


def filter_by_bbox(institutions: SQLAlchemyQuery, bbox: str | None) -> SQLAlchemyQuery:
    if not bbox:
        return institutions
    bbox_polygon_wkt = bbox_str_to_polygon_wkt(bbox)
    return institutions.filter(
        SecondarySchoolInstitution.geometry.ST_Within(
            func.ST_GeomFromText(bbox_polygon_wkt, 4326)
        )
    )


def filter_by_points_threshold(
    institutions: SQLAlchemyQuery, points_threshold: list[int] | None
) -> SQLAlchemyQuery:
    if not points_threshold or len(points_threshold) != 2:
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


def filter_by_extended_subjects(
    institutions: SQLAlchemyQuery, extended_subjects_list: list[list[str]] | None
) -> SQLAlchemyQuery:
    if not extended_subjects_list:
        return institutions

    conditions = [
        and_(
            SecondarySchoolInstitutionClass.extended_subjects.contains(
                extended_subjects_per_class
            ),
            SecondarySchoolInstitutionClass.extended_subjects.contained_by(
                extended_subjects_per_class
            ),
            RspoInstitution.rspo == SecondarySchoolInstitutionClass.institution_rspo,
            SecondarySchoolInstitutionClass.year == INSTITUTION_CLASSES_CURRENT_YEAR,
        )
        for extended_subjects_per_class in extended_subjects_list
    ]

    return institutions.filter(SecondarySchoolInstitution.classes.any(or_(*conditions)))


def filter_by_public_transport_route_type(
    institutions: SQLAlchemyQuery, public_transport_route_type: list[str] | None
) -> SQLAlchemyQuery:
    if not public_transport_route_type:
        return institutions
    return institutions.filter(
        PublicTransportStop.public_transport_routes.any(
            PublicTransportRoute.type.in_(public_transport_route_type)
        )
    )


def filter_institutions(
    db: Session, filters_query: FiltersQuerySchema
) -> SQLAlchemyQuery:
    institutions: SQLAlchemyQuery = query_institutions(db, with_public_transport=True)

    institutions = filter_by_project_id(institutions, filters_query.project_id)

    institutions = filter_by_query(institutions, filters_query.query)

    institutions = filter_by_languages(institutions, filters_query.languages)

    institutions = filter_by_points_threshold(
        institutions, filters_query.points_threshold
    )

    institutions = filter_by_is_public(institutions, filters_query.is_public)

    institutions = filter_by_rspo_institution_type(
        institutions, filters_query.rspo_institution_type
    )

    institutions = filter_by_extended_subjects(
        institutions, filters_query.extended_subjects
    )

    institutions = filter_by_public_transport_route_type(
        institutions, filters_query.public_transport_route_type
    )

    institutions = filter_by_bbox(institutions, filters_query.bbox)

    return institutions
