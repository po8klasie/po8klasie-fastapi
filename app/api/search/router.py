from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.api.search.filtering import (
    filter_by_query,
    filter_by_project_id,
    search_router_secondary_school_entities,
    filter_institutions,
)
from app.api.search.map_features import (
    road_accident_models_to_features,
    bbox_regex,
    bbox_str_to_polygon_wkt,
    institution_models_to_features,
)
from app.institution.models import (
    SecondarySchoolInstitution,
    query_secondary_school_institutions,
)
from app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
    query_current_classes,
)
from app.rspo_institution.models import RspoInstitution

from db.models import RoadAccident
from db.db import get_db
from geojson import (
    FeatureCollection as GeoJsonFeatureCollection,
)

search_router = APIRouter()


@search_router.get("/autocomplete")
def route_search_autocomplete(
    query: str = Query(default=...), project_id: str = "", db: Session = Depends(get_db)
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

    if project_id:
        institutions = filter_by_project_id(institutions, project_id)

    return institutions.limit(5).all()


@search_router.get("/institution/{rspo}")
def route_search_single_institution(
    rspo: str = Query(default=...), db: Session = Depends(get_db)
):
    institution = (
        query_secondary_school_institutions(db, search_router_secondary_school_entities)
        .filter(SecondarySchoolInstitution.rspo == rspo)
        .one_or_none()
    )

    if not institution:
        raise HTTPException(
            status_code=404,
            detail={"success": False, "message": "Institution not found"},
        )

    return institution


@search_router.get("/institution")
def route_search_institutions(
    bbox: str = Query(default=None, regex=bbox_regex),
    project_id: str = None,
    is_public: bool | None = None,
    query: str | None = None,
    languages: List[str] = Query(None),
    points_threshold: List[int] = Query(None),
    rspo_institution_type: List[str] = Query(None),
    db: Session = Depends(get_db),
):
    institutions = filter_institutions(
        db,
        query=query,
        project_id=project_id,
        is_public=is_public,
        languages=languages,
        points_threshold=points_threshold,
        rspo_institution_type=rspo_institution_type,
        bbox=bbox,
    ).order_by(
        func.array_length(SecondarySchoolInstitution.available_extended_subjects, 1)
        == 0,
        desc(
            func.array_length(SecondarySchoolInstitution.available_extended_subjects, 1)
        ),
    )

    institutions = institutions.all()

    # TODO(micorix): Come up with more efficient way of doing this
    for institution in institutions:
        classes = (
            query_current_classes(db)
            .with_entities(SecondarySchoolInstitutionClass.extended_subjects)
            .filter(
                SecondarySchoolInstitutionClass.institution_rspo == institution.rspo
            )
            .all()
        )

        yield {**dict(institution), "classes": classes}


@search_router.get("/map_features")
def route_search_map_features(
    bbox: str = Query(default=None, regex=bbox_regex),
    project_id: str = None,
    is_public: bool | None = None,
    query: str | None = None,
    languages: List[str] = Query(None),
    points_threshold: List[int] = Query(None),
    rspo_institution_type: List[str] = Query(None),
    layers_ids: List[str] = Query(None),
    db: Session = Depends(get_db),
):

    response = {"institutions": None, "roadAccidents": None}

    institutions = (
        filter_institutions(
            db,
            query=query,
            project_id=project_id,
            is_public=is_public,
            languages=languages,
            points_threshold=points_threshold,
            rspo_institution_type=rspo_institution_type,
            bbox=bbox,
        )
        .with_entities(
            SecondarySchoolInstitution.rspo,
            RspoInstitution.name,
            SecondarySchoolInstitution.geometry,
        )
        .all()
    )

    response["institutions"] = GeoJsonFeatureCollection(
        institution_models_to_features(institutions)
    )

    if bbox and layers_ids and "roadAccidents" in layers_ids:
        print("road acc")
        bbox_polygon_wkt = bbox_str_to_polygon_wkt(bbox)
        road_accidents = (
            db.query(RoadAccident)
            .filter(RoadAccident.geometry.ST_Within(bbox_polygon_wkt))
            .all()
        )
        response["roadAccidents"] = GeoJsonFeatureCollection(
            road_accident_models_to_features(road_accidents)
        )

    return response
