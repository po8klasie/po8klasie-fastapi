from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, ARRAY, Date, Boolean
from app.db.base import Base


class RspoSubfieldMapping(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String)


class RspoEntityType(RspoSubfieldMapping):
    __tablename__ = "rspo_entity_types"


class RspoFacilityLegalStatus(RspoSubfieldMapping):
    __tablename__ = "rspo_facility_legal_statuses"


class RspoEducationalLevel(RspoSubfieldMapping):
    __tablename__ = "rspo_educational_levels"


class RspoStudentsCategory(RspoSubfieldMapping):
    __tablename__ = "rspo_students_categories"


class RspoFacilityBindingType(RspoSubfieldMapping):
    __tablename__ = "rspo_facility_binding_types"


class RspoReportingEntity(Base):
    __tablename__ = "rspo_reporting_entities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    regon = Column(String)
    entity_type = relationship("RspoEntityType")
    entity_type_id = Column(Integer, ForeignKey("rspo_entity_types.id"))


class RspoFacilityOwnerEntity(Base):
    __tablename__ = "rspo_facility_owner_entities"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    regon = Column(String)
    entity_type = relationship("RspoEntityType")
    entity_type_id = Column(Integer, ForeignKey("rspo_entity_types.id"))


class RspoFacility(Base):
    __tablename__ = "rspo_facilities"

    project = relationship("Project")
    project_id = Column(String, ForeignKey("projects.project_id"))

    # numerRspo
    rspo = Column(String, primary_key=True)

    # dataZalozenia
    foundation_date = Column(Date)
    # dataRozpoczecia
    commencement_date = Column(Date)
    # dataZakonczenia
    shutdown_date = Column(Date)
    # dataLikwidacji
    termination_date = Column(Date)
    # dataWlaczeniaDoZespolu
    complex_inclusion_date = Column(Date)
    # dataWylaczeniaZZespolu
    complex_exclusion_date = Column(Date)

    # nip
    nip = Column(String)
    # regon
    regon = Column(String)

    # nazwa
    name = Column(String)
    # nazwaSkrocona
    shortened_name = Column(String)

    facility_type = relationship("RspoEntityType")
    facility_type_id = Column(Integer, ForeignKey("rspo_entity_types.id"))

    # dyrektorImie
    principal_first_name = Column(String)
    # dyrektorNazwisko
    principal_last_name = Column(String)

    # statusPublicznoPrawny
    facility_legal_status = relationship("RspoFacilityLegalStatus")
    facility_legal_status_id = Column(
        Integer, ForeignKey("rspo_facility_legal_statuses.id")
    )
    # kategoriaUczniow
    students_category = relationship("RspoStudentsCategory")
    students_category_id = Column(Integer, ForeignKey("rspo_students_categories.id"))
    # specyfikaSzkoly
    school_specifics = Column(ARRAY(String))
    # zwiazanieOrganizacyjne
    facility_binding_type = relationship("RspoFacilityBindingType")
    facility_binding_type_id = Column(
        Integer, ForeignKey("rspo_facility_binding_types.id")
    )

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

    # podmiotPrzekazujacyDaneDoRSPO
    reporting_entity = relationship("RspoReportingEntity")
    reporting_entity_id = Column(Integer, ForeignKey("rspo_reporting_entities.id"))
    # podmiotProwadzacy
    facility_owner_entity = relationship("RspoFacilityOwnerEntity")
    facility_owner_entity_id = Column(
        Integer, ForeignKey("rspo_facility_owner_entities.id")
    )
    # podmiotNadrzedny
    parent_entity = Column(String)
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

    # adresDoKorespondecjiMiejscowosc
    forwarding_address_city = Column(String)
    # adresDoKorespondecjiUlica
    forwarding_address_street = Column(String)
    # adresDoKorespondecjiNumerBudynku
    forwarding_address_building_no = Column(String)
    # adresDoKorespondecjiNumerLokalu
    forwarding_address_apartment_no = Column(String)
    # adresDoKorespondecjiKodPocztowy
    forwarding_address_postal_code = Column(String)

    # placowkiPodrzedne
    dependent_facilities = Column(ARRAY(String))
