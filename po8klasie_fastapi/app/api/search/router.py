from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from geojson import FeatureCollection as GeoJsonFeatureCollection
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.search.filtering import (
    FiltersQuerySchema,
    filter_by_project_id,
    filter_by_query,
    filter_institutions,
    search_router_secondary_school_entities,
)
from po8klasie_fastapi.app.api.search.map_features import (
    bbox_str_to_polygon_wkt,
    get_road_accidents_collection,
    institution_models_to_features,
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
from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
)
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution
from po8klasie_fastapi.db.db import get_db

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
    try:
        return (
            query_secondary_school_institutions(
                db, search_router_secondary_school_entities
            )
            .filter(SecondarySchoolInstitution.rspo == rspo)
            .one()
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail={"success": False, "message": "Institution not found"},
        )


@search_router.get("/institution")
def route_search_institutions(
    filters_query: FiltersQuerySchema = Depends(),
    db: Session = Depends(get_db),
):
    institutions = filter_institutions(db, filters_query)
    institutions = order_institutions(institutions)

    institutions_with_classes = (
        institutions.join(RspoInstitution)
        .join(SecondarySchoolInstitutionClass)
        .filter(SecondarySchoolInstitutionClass.year == 2022)
        .with_entities(
            RspoInstitution,
            SecondarySchoolInstitution,
            SecondarySchoolInstitutionClass.extended_subjects,
        )
        .all()
    )

    for rspo_institution, institution, classes in institutions_with_classes:
        yield {
            **RspoInstitutionSchema.from_orm(rspo_institution).dict(),
            **SecondarySchoolInstitutionSchema.from_orm(institution).dict(),
            "classes": classes,
        }


@search_router.get("/map_features")
def route_search_map_features(
    filters_query: FiltersQuerySchema = Depends(),
    layers_ids: List[str] = Query(None),
    db: Session = Depends(get_db),
):
    bbox = filters_query.bbox

    if not bbox:
        raise HTTPException(status_code=422)

    def is_layer_enabled(layer_id: str):
        return bbox and layers_ids and layer_id in layers_ids

    def get_layer(layer_id, func):
        if is_layer_enabled(layer_id):
            bbox_polygon_wkt = bbox_str_to_polygon_wkt(bbox)
            return func(db=db, bbox_polygon_wkt=bbox_polygon_wkt)
        return GeoJsonFeatureCollection([])

    institutions = (
        filter_institutions(db, filters_query)
        .with_entities(
            SecondarySchoolInstitution.rspo,
            RspoInstitution.name,
            SecondarySchoolInstitution.geometry,
        )
        .all()
    )
    institutions_collection = GeoJsonFeatureCollection(
        institution_models_to_features(institutions)
    )

    return {
        "institutions": institutions_collection,
        "roadAccidents": get_layer("roadAccidents", get_road_accidents_collection),
    }
