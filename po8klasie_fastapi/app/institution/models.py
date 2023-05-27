import enum

from geoalchemy2 import Geometry
from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, and_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import (
    Session,
    relationship,
    contains_eager,
    Query as SQLAlchemyQuery,
)
from po8klasie_fastapi.db.base import Base

from po8klasie_fastapi.app.institution_classes.consts import (
    INSTITUTION_CLASSES_CURRENT_YEAR,
)
from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
)
from po8klasie_fastapi.app.public_transport_info.models import (
    InstitutionPublicTransportStopAssociation,
    PublicTransportRoute,
    PublicTransportStop,
)
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution

import po8klasie_fastapi.app.rankings.zwzt.models


class InstitutionTypeGeneralizedEnum(enum.Enum):
    SECONDARY_SCHOOL = "secondary_school"


class Institution(Base):
    __tablename__ = "institutions"

    project = relationship("Project")
    project_id = Column(String, ForeignKey("projects.project_id"))

    rspo_institution: RspoInstitution = relationship("RspoInstitution")
    rspo = Column(String, ForeignKey("rspo_institutions.rspo"), primary_key=True)

    institution_type_generalized = Column(Enum(InstitutionTypeGeneralizedEnum))

    public_transport_stops = relationship(
        "InstitutionPublicTransportStopAssociation", back_populates="institution"
    )

    geometry = Column(Geometry("POINT", srid=4326))

    __mapper_args__ = {"polymorphic_on": institution_type_generalized}


class SecondarySchoolInstitution(Institution):
    __tablename__ = "secondary_school_institutions"

    __mapper_args__ = {
        "polymorphic_identity": InstitutionTypeGeneralizedEnum.SECONDARY_SCHOOL
    }

    rspo = Column(None, ForeignKey("institutions.rspo"), primary_key=True)

    classes = relationship(
        "SecondarySchoolInstitutionClass", back_populates="institution"
    )

    zwzt_ranking_entries = relationship(
        "ZwzTRankingEntry", back_populates="institution"
    )

    points_stats_min = Column(Float)
    points_stats_max = Column(Float)
    available_languages = Column(ARRAY(String))
    available_extended_subjects = Column(ARRAY(String))

    classrooms_count = Column(Integer)
    sport_classes_count = Column(Integer)
    working_time = Column(String)
    students_per_teacher = Column(Float)

    description = Column(String)

    extracurricular_activities = Column(ARRAY(String))
    school_events = Column(ARRAY(String))

    sport_infrastructure = Column(ARRAY(String))
    sport_activities = Column(ARRAY(String))

    NGO_partners = Column(ARRAY(String))
    university_partners = Column(ARRAY(String))

    avg_students_no_per_class = Column(Integer)
    max_students_no_per_class = Column(Integer)
    min_students_no_per_class = Column(Integer)

    no_of_students_taking_part_in_olympiads = Column(String)
    no_of_internal_competitions = Column(String)
    no_of_school_trips_per_year = Column(String)
    no_of_fulltime_psychologist_positions = Column(Float)


classes_base_filters = [
    RspoInstitution.rspo == SecondarySchoolInstitutionClass.institution_rspo,
    SecondarySchoolInstitutionClass.year == INSTITUTION_CLASSES_CURRENT_YEAR,
]


def query_institutions(
    db: Session, with_public_transport: bool = False
) -> SQLAlchemyQuery:
    institutions = db.query(SecondarySchoolInstitution).join(RspoInstitution)

    institutions = (
        institutions.outerjoin(
            SecondarySchoolInstitutionClass, and_(*classes_base_filters)
        )
        .options(contains_eager(SecondarySchoolInstitution.classes))
        .populate_existing()
    )

    if with_public_transport:
        institutions = institutions.outerjoin(
            InstitutionPublicTransportStopAssociation,
            PublicTransportStop,
            PublicTransportRoute,
        )

    return institutions
