from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Float,
    Integer,
    Enum,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Session

from db.base import Base

from app.rspo_institution.models import RspoInstitution

import enum


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

    __mapper_args__ = {"polymorphic_on": institution_type_generalized}


class SecondarySchoolInstitution(Institution):
    __tablename__ = "secondary_school_institutions"

    __mapper_args__ = {
        "polymorphic_identity": InstitutionTypeGeneralizedEnum.SECONDARY_SCHOOL
    }

    rspo = Column(None, ForeignKey("institutions.rspo"), primary_key=True)

    classrooms_count = Column(Integer)
    sport_classes_count = Column(Integer)
    working_time = Column(String)
    students_per_teacher = Column(Float)
    description = Column(String)
    sport_activities = Column(ARRAY(String))
    foreign_languages = Column(ARRAY(String))
    class_profiles = Column(ARRAY(String))
    extracurricular_activities = Column(ARRAY(String))


def query_institutions(db: Session, entities):
    return (
        db.query(Institution)
        .join(Institution.rspo_institution)
        .with_entities(*entities)
    )


def query_secondary_school_institutions(db: Session, entities):
    return (
        db.query(SecondarySchoolInstitution)
        .join(SecondarySchoolInstitution.rspo_institution)
        .with_entities(*entities)
    )
