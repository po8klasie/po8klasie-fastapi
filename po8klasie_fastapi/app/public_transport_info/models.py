from sqlalchemy import Column, Float, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from po8klasie_fastapi.db.base import Base

public_transport_stop_route_association_table = Table(
    "public_transport_stop_route_association",
    Base.metadata,
    Column(
        "public_transport_stop_osm_id",
        ForeignKey("public_transport_stops.osm_id"),
        primary_key=True,
    ),
    Column(
        "public_transport_route_osm_id",
        ForeignKey("public_transport_routes.osm_id"),
        primary_key=True,
    ),
)


class InstitutionPublicTransportStopAssociation(Base):
    __tablename__ = "institution_public_transport_stop_association"
    public_transport_stop_osm_id = Column(
        ForeignKey("public_transport_stops.osm_id"), primary_key=True
    )
    institution_rspo = Column(ForeignKey("institutions.rspo"), primary_key=True)

    institution = relationship("Institution")
    public_transport_stop = relationship("PublicTransportStop")

    distance = Column(Float)
    radius = Column(Integer)


class PublicTransportRoute(Base):
    __tablename__ = "public_transport_routes"

    public_transport_stop_osm_id = Column(
        String, ForeignKey("public_transport_stops.osm_id")
    )

    osm_id = Column(String, primary_key=True)
    name = Column(String)
    route_from = Column(String)
    route_to = Column(String)
    ref = Column(String)
    type = Column(String)
    operator = Column(String)

    public_transport_stops = relationship(
        "PublicTransportStop",
        secondary=public_transport_stop_route_association_table,
        back_populates="public_transport_routes",
    )


class PublicTransportStop(Base):
    __tablename__ = "public_transport_stops"

    osm_id = Column(String, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    public_transport_routes = relationship(
        "PublicTransportRoute",
        secondary=public_transport_stop_route_association_table,
        back_populates="public_transport_stops",
    )

    institutions = relationship(
        "InstitutionPublicTransportStopAssociation",
        back_populates="public_transport_stop",
    )
