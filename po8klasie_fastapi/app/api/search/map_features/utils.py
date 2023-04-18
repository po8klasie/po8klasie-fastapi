import re
from typing import Iterable

import morecantile
from morecantile import Tile
from sqlalchemy import func, text

from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.public_transport_info.models import (
    InstitutionPublicTransportStopAssociation,
    PublicTransportStop,
)

# MVT utils


def prepare_mvt_statement(tile: Tile, input_stmt, columns_to_select: list[str]):
    tms = morecantile.tms.get("WebMercatorQuad")
    bbox = tms.xy_bounds(tile)
    xmin = bbox.left
    ymin = bbox.bottom
    xmax = bbox.right
    ymax = bbox.top
    epsg = tms.crs.to_epsg()

    selected_columns = ", ".join(["geom", *columns_to_select])

    stmt = text(
        f"""
        SELECT ST_AsMVT(mvtgeom.*) FROM (
            SELECT ST_asmvtgeom(ST_Transform(t.geom, 3857), bounds.geom) AS {selected_columns}
            FROM ({input_stmt}) t,
                (SELECT ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, :epsg) as geom) bounds
            WHERE ST_Intersects(t.geom, ST_Transform(bounds.geom, 4326))
        ) mvtgeom;
    """
    )

    stmt = stmt.bindparams(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, epsg=epsg)
    return stmt


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
