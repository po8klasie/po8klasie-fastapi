from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response
from morecantile import Tile
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.search.filtering import FiltersQuery, filter_institutions
from po8klasie_fastapi.app.api.search.map_features.utils import (
    get_institutions_bounds_array,
    get_institutions_near_stop,
    get_stop_routes,
    query_mvt_tiles,
)
from po8klasie_fastapi.app.config import settings
from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.public_transport_info.models import (
    InstitutionPublicTransportStopAssociation,
    PublicTransportRoute,
    PublicTransportStop,
)
from po8klasie_fastapi.app.road_accident.models import RoadAccident
from po8klasie_fastapi.db.db import get_db

search_map_features_router = APIRouter()


class MVTResponse(Response):
    def __init__(self, tiles):
        super().__init__(bytes(tiles), media_type="application/x-protobuf")


def tile_params(
    z: int = Path(
        ...,
        ge=0,
        le=25,
    ),
    x: int = Path(...),
    y: int = Path(...),
) -> Tile:
    """Tile parameters."""
    return Tile(x, y, z)


@search_map_features_router.get("/institutions/tilejson")
def route_institutions_tilejson(
    filters_query: Annotated[FiltersQuery, Depends(FiltersQuery)],
    db: Session = Depends(get_db),
):
    filters_model = filters_query.model

    institutions = filter_institutions(db, filters_model).with_entities(
        SecondarySchoolInstitution.rspo,
        SecondarySchoolInstitution.geometry,
    )

    bounds: list[float] | None = get_institutions_bounds_array(
        db, institutions.subquery()
    )
    tile_url_params = filters_query.get_qs()
    print(tile_url_params)

    return {
        "tilejson": "2.0.0",
        "name": "institutions",
        "attribution": "",
        "bounds": bounds,
        "format": "mvt",
        "type": "layer",
        "tiles": [
            settings.site_url
            + "/api/search/map_features/institutions/tiles/{z}/{x}/{y}?"
            + tile_url_params
        ],
    }


@search_map_features_router.get("/institutions/tiles/{z}/{x}/{y}/")
def route_institutions_tiles(
    filters_query: Annotated[FiltersQuery, Depends(FiltersQuery)],
    tile: Tile = Depends(tile_params),
    db: Session = Depends(get_db),
):
    result = query_mvt_tiles(
        db,
        tile,
        SecondarySchoolInstitution.geometry,
        columns_to_select=[SecondarySchoolInstitution.rspo],
        joins=[filter_institutions(db, filters_query.model).subquery()],
    )

    return MVTResponse(result)


@search_map_features_router.get("/road_accidents/tiles/{z}/{x}/{y}/")
def road_accidents_tiles(
    tile: Tile = Depends(tile_params),
    db: Session = Depends(get_db),
):
    result = query_mvt_tiles(
        db,
        tile,
        RoadAccident.geometry,
        columns_to_select=[RoadAccident.sewik_id.label("sewikid")],
    )

    return MVTResponse(result)


@search_map_features_router.get("/public_transport_stops/tiles/{z}/{x}/{y}/")
def public_transport_stops_tiles(
    tile: Tile = Depends(tile_params),
    db: Session = Depends(get_db),
):
    result = query_mvt_tiles(
        db,
        tile,
        PublicTransportStop.geometry,
        columns_to_select=[
            PublicTransportStop.name,
            PublicTransportStop.osm_id.label("osmid"),
        ],
    )

    return MVTResponse(result)


@search_map_features_router.get("/public_transport_stops/stop_popup_info/{osm_id}")
def public_transport_stop_popup_info(
    osm_id: str = Path(),
    db: Session = Depends(get_db),
):
    try:
        stop = (
            db.query(PublicTransportStop)
            .outerjoin(InstitutionPublicTransportStopAssociation, PublicTransportRoute)
            .filter(PublicTransportStop.osm_id == osm_id)
            .one()
        )
    except NoResultFound:
        raise HTTPException(status_code=404)

    return {
        "featureType": "public_transport_stop",
        "name": stop.name,
        "institutions": list(get_institutions_near_stop(stop.institutions)),
        "routes": list(get_stop_routes(stop)),
    }
