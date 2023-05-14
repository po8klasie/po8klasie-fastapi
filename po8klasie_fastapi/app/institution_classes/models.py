import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from po8klasie_fastapi.app.institution_classes.consts import (
    INSTITUTION_CLASSES_CURRENT_YEAR,
)
from po8klasie_fastapi.db.base import Base


class SecondarySchoolInstitutionClass(Base):
    __tablename__ = "institution_classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    year = Column(Integer)

    class_name = Column(String)
    class_symbol = Column(String)

    class_type = Column(String)
    class_size = Column(String)

    occupation = Column(String)

    description = Column(String)

    available_languages = Column(ARRAY(String))
    extended_subjects = Column(ARRAY(String))

    points_stats_min = Column(Float)
    points_stats_avg = Column(Float)
    points_stats_max = Column(Float)

    url = Column(String)

    institution_rspo = Column(String, ForeignKey("secondary_school_institutions.rspo"))
    institution = relationship("SecondarySchoolInstitution", back_populates="classes")


def query_current_classes(db):
    return db.query(SecondarySchoolInstitutionClass).filter(
        SecondarySchoolInstitutionClass.year == INSTITUTION_CLASSES_CURRENT_YEAR
    )
