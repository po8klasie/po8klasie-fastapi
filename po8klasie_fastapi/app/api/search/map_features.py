from typing import Iterable

from geojson import Feature as GeoJsonFeature, Point as GeoJsonPoint

from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.road_accident.models import RoadAccident


import shapely.geometry

from po8klasie_fastapi.db.postgis_utils import get_point_coords

bbox_regex = r"^\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+$"


def bbox_str_to_polygon_wkt(bbox_str: str) -> str:
    bbox = map(float, bbox_str.split(","))
    polygon = shapely.geometry.box(*bbox, ccw=True)
    return polygon.wkt


def road_accident_models_to_features(road_accidents: Iterable[RoadAccident]):
    for road_accident in road_accidents:
        yield GeoJsonFeature(
            properties={
                "featureType": "roadAccident",
                "sewikId": road_accident.sewik_id,
            },
            geometry=GeoJsonPoint(get_point_coords(road_accident.geometry)),
        )


def institution_models_to_features(institutions: Iterable[SecondarySchoolInstitution]):
    for institution in institutions:
        properties = {
            "featureType": "institution",
            "rspo": institution.rspo,
            "name": institution.name,
        }

        yield GeoJsonFeature(
            properties=properties,
            geometry=GeoJsonPoint(get_point_coords(institution.geometry)),
        )
