import re
from typing import Iterable

import morecantile
from geoalchemy2 import Geometry
from morecantile import Tile
from sqlalchemy import and_, column, func
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression

from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.public_transport_info.models import (
    InstitutionPublicTransportStopAssociation,
    PublicTransportStop,
)

# MVT utils


def query_mvt_tiles(
    db: Session,
    tile: Tile,
    geometry_column: Geometry,
    columns_to_select: list[str] = (),
    joins: list[expression] = (),
):
    tms = morecantile.tms.get("WebMercatorQuad")
    bbox = tms.xy_bounds(tile)
    xmin = bbox.left
    ymin = bbox.bottom
    xmax = bbox.right
    ymax = bbox.top
    epsg = tms.crs.to_epsg()

    subquery = db.query(
        func.ST_AsMVTGeom(
            func.ST_Transform(geometry_column, 3857),
            func.ST_MakeEnvelope(xmin, ymin, xmax, ymax, epsg),
        ).label("geom"),
        *columns_to_select
    )

    if len(joins):
        subquery = subquery.join(*joins)
    subquery = subquery.filter(
        and_(
            func.ST_Intersects(
                geometry_column,
                func.ST_Transform(
                    func.ST_MakeEnvelope(xmin, ymin, xmax, ymax, epsg), 4326
                ),
            ),
        )
    ).subquery("mvtgeom")

    return (
        db.query(func.ST_AsMVT(column("mvtgeom"), "layer", 4096, "geom"))
        .select_from(subquery)
        .scalar()
    )


# bounds utils


def box_wkt_to_bounds_array(bbox_wkt_str: str) -> list[float] | None:
    if not bbox_wkt_str:
        return None
    bbox: str = re.match(r"BOX\((.*)\)", bbox_wkt_str).group(1)
    bbox: list[str] = re.split(r"\s|,", bbox)
    bbox: list[float] = list(map(float, bbox))
    return bbox


def get_institutions_bounds_array(db, subquery):
    bbox_wkt = (
        db.query(
            func.ST_Extent(SecondarySchoolInstitution.geometry).label("table_extent")
        )
        .join(subquery)
        .one()
        .table_extent
    )
    return box_wkt_to_bounds_array(bbox_wkt)


# public transport stop mappings


def get_institutions_near_stop(
    assocs: Iterable[InstitutionPublicTransportStopAssociation],
):
    for assoc in assocs:
        yield {
            "name": assoc.institution.rspo_institution.name,
            "rspo": assoc.institution_rspo,
            "distance": assoc.distance,
        }


def get_stop_routes(stop: PublicTransportStop):
    for route in stop.public_transport_routes:
        yield {
            "name": route.name,
            "ref": route.ref,
            "routeFrom": route.route_from,
            "routeTo": route.route_to,
            "type": route.type,
        }
