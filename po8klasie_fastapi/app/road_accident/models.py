from geoalchemy2 import Geometry
from sqlalchemy import Column, String

from po8klasie_fastapi.db.base import Base


class RoadAccident(Base):
    __tablename__ = "road_accidents"

    sewik_id = Column(String, primary_key=True)
    accident_type_id = Column(String)
    geometry = Column(Geometry("POINT", srid=4326))
