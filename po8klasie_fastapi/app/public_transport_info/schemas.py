from typing import List, Optional

from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel


class PublicTransportRouteSchema(CamelCasedModel):
    name: str
    route_from: Optional[str]
    route_to: Optional[str]
    ref: Optional[str]
    type: str
    operator: Optional[str]

    class Config:
        orm_mode = True


class PublicTransportStopSchema(CamelCasedModel):
    name: str
    latitude: float
    longitude: float

    public_transport_routes: List[PublicTransportRouteSchema]

    class Config:
        orm_mode = True


class InstitutionPublicTransportStopAssociationSchema(CamelCasedModel):
    distance: float

    public_transport_stop: PublicTransportStopSchema

    class Config:
        orm_mode = True
