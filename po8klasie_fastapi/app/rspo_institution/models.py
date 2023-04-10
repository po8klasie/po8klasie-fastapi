from sqlalchemy import ARRAY, Boolean, Column, Date, Float, String

from po8klasie_fastapi.db.base import Base


class RspoInstitution(Base):
    __tablename__ = "rspo_institutions"

    # numerRspo
    rspo = Column(String, primary_key=True)
    rspo_institution_type = Column(String)

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

    institution_type = Column(String)

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
