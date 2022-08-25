from typing import Optional

from sqlalchemy import Column, ForeignKey, String, Date, ARRAY, Float, Boolean, Integer
from sqlalchemy.orm import relationship, Session

from db.base import Base


class Facility(Base):
    __tablename__ = "facilities"

    project = relationship("Project")
    project_id = Column(String, ForeignKey("projects.project_id"))

    # numerRspo
    rspo = Column(String, primary_key=True)
    rspo_facility_type = Column(String)

    # dataZalozenia
    foundation_date = Column(Date)
    # dataRozpoczecia
    commencement_date = Column(Date)
    # dataZakonczenia
    shutdown_date = Column(Date)
    # dataLikwidacji
    termination_date = Column(Date)

    is_public = Column(Boolean)

    # nip
    nip = Column(String)
    # regon
    regon = Column(String)

    # nazwa
    name = Column(String)
    # nazwaSkrocona
    shortened_name = Column(String)

    facility_type = Column(String)

    # dyrektorImie
    principal_first_name = Column(String)
    # dyrektorNazwisko
    principal_last_name = Column(String)

    # czyPosiadaObwod
    has_school_area = Column(Boolean)
    # czyPosiadaInternat
    has_dormitory = Column(Boolean)
    # czyDotacjaWPrzyszlymRoku
    next_year_subsidy = Column(Boolean)
    # opiekaDydaktycznoNaukowaUczelni"
    partner_universities = Column(ARRAY(String))

    # ksztalcenieZawodowe
    vocational_training = Column(ARRAY(String))
    # ksztalcenieZawodoweProfilowane
    vocational_profiled_training = Column(ARRAY(String))
    # ksztalcenieZawodoweArtystyczne
    vocational_art_training = Column(ARRAY(String))
    # ksztalcenieNKJO
    nkjo_training = Column(ARRAY(String))
    # ksztalcenieWKolegiachNauczycielskich
    teacher_training = Column(ARRAY(String))
    # ksztalcenieWkolegiachPracownikowSluzbSpolecznych
    social_service_worker_training = Column(ARRAY(String))

    # wojewodztwo
    voivodeship = Column(String)
    # wojewodztwoKodTERYT
    voivodeship_code = Column(String)
    # powiat
    county = Column(String)
    # powiatKodTERYT
    county_code = Column(String)
    # gmina
    borough = Column(String)
    # gminaKodTERYT
    borough_code = Column(String)
    # miejscowosc
    city = Column(String)
    # miejscowoscKodTERYT
    city_code = Column(String)
    # ulica
    street = Column(String)
    # ulicaKodTERYT
    street_code = Column(String)
    # numerBudynku
    building_number = Column(String)
    # numerLokalu
    apartment_number = Column(String)
    # kodPocztowy
    postal_code = Column(String)

    # geolokalizacja.latitude
    latitude = Column(Float)
    # geolokalizacja.longitude
    longitude = Column(Float)

    # telefon
    phone = Column(String)
    # email
    email = Column(String)
    # stronaInternetowa
    website = Column(String)

    classrooms_count = Column(Integer)
    sport_classes_count = Column(Integer)
    working_time = Column(String)
    students_per_teacher = Column(Float)
    description = Column(String)
    sport_activities = Column(ARRAY(String))
    foreign_languages = Column(ARRAY(String))
    class_profiles = Column(ARRAY(String))
    extracurricular_activities = Column(ARRAY(String))


def query_facility(db: Session):
    return db.query(Facility)


def get_facilities(db: Session, project_id: Optional[str] = None):
    query = query_facility(db)
    if project_id:
        query = query.filter_by(project_id=project_id)
    return query


def get_facility(db: Session, rspo: str):
    return query_facility(db).filter_by(rspo=rspo).one()
