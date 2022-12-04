from sqlalchemy import Column, String

from db.base import Base
from geoalchemy2 import Geometry


class RoadAccident(Base):
    __tablename__ = "road_accidents"

    sewik_id = Column(String, primary_key=True)
    accident_type_id = Column(String)
    geometry = Column(Geometry("POINT"))
