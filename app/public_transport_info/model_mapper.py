import overpy
from sqlalchemy.exc import NoResultFound

from app.public_transport_info.models import (
    PublicTransportStop,
    PublicTransportRoute,
    InstitutionPublicTransportStopAssociation,
)
from geopy import distance as geopy_distance

api = overpy.Overpass()

overpass_query = """
        (
            node(around:{radius},{lat},{lng})["public_transport"="stop_position"];
            relation(bn)["route"];
        );
        out body;
"""


def get_nearby_stops_and_routes(radius, lat, lng):
    return api.query(overpass_query.format(radius=radius, lat=lat, lng=lng))


def map_node_to_public_transport_stop(db, node):
    osm_id = str(node.id)
    try:
        stop_match = db.query(PublicTransportStop).filter_by(osm_id=osm_id).one()
        return stop_match
    except NoResultFound:
        return PublicTransportStop(
            osm_id=osm_id,
            name=node.tags.get("name"),
            latitude=node.lat,
            longitude=node.lon,
        )


def map_relation_to_public_transport_route(db, relation):
    osm_id = str(relation.id)

    try:
        route_match = db.query(PublicTransportRoute).filter_by(osm_id=osm_id).one()
        return route_match
    except NoResultFound:
        return PublicTransportRoute(
            osm_id=osm_id,
            name=relation.tags.get("name"),
            route_from=relation.tags.get("from"),
            route_to=relation.tags.get("to"),
            ref=relation.tags.get("ref"),
            type=relation.tags.get("route"),
            operator=relation.tags.get("operator"),
        )


def get_stop_id_from_relation_members(members, stop_ids):
    member_ids = set(str(member.ref) for member in members)
    return next(iter(stop_ids.intersection(member_ids) or []), None)


def calc_distance(model1, model2):
    return geopy_distance.geodesic(
        (model1.longitude, model1.latitude), (model2.longitude, model2.latitude)
    ).meters


def add_public_transport_stops_data_to_institution(db, institution, radius):
    result = get_nearby_stops_and_routes(
        radius=radius, lat=institution.latitude, lng=institution.longitude
    )

    stops_mapping = {}

    for node in result.nodes:
        stop = map_node_to_public_transport_stop(db, node)
        stops_mapping[stop.osm_id] = stop

    stop_ids = set(stops_mapping.keys())

    for relation in result.relations:
        stop_id = get_stop_id_from_relation_members(
            members=relation.members, stop_ids=stop_ids
        )

        if any([not stop_id, stop_id not in stops_mapping]):
            continue

        route = map_relation_to_public_transport_route(db, relation)

        stops_mapping[stop_id].public_transport_routes.append(route)

    for stop in stops_mapping.values():
        assoc = InstitutionPublicTransportStopAssociation()
        assoc.distance = calc_distance(institution, stop)
        assoc.public_transport_stop = stop
        assoc.radius = radius
        institution.public_transport_stops.append(assoc)

    return institution
