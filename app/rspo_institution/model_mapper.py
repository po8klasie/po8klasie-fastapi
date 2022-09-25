from typing import Dict

from app.rspo_institution.models import RspoInstitution


def create_model_from_rspo_institution_data(fd: Dict):
    rspo_institution = RspoInstitution(
        rspo=str(fd.get("numerRspo")),
        rspo_institution_type=fd.get("typ", {}).get("id"),
        foundation_date=fd.get("dataZalozenia"),
        commencement_date=fd.get("dataRozpoczecia"),
        shutdown_date=fd.get("dataZakonczenia"),
        termination_date=fd.get("dataLikwidacji"),
        nip=fd.get("nip"),
        regon=fd.get("regon"),
        name=fd.get("nazwa"),
        shortened_name=fd.get("nazwaSkrocona"),
        is_public=fd.get("statusPublicznoPrawny", {}).get("nazwa") == "publiczna",
        principal_first_name=fd.get("dyrektorImie"),
        principal_last_name=fd.get("dyrektorNazwisko"),
        has_school_area=fd.get("czyPosiadaObwod"),
        has_dormitory=fd.get("czyPosiadaInternat"),
        next_year_subsidy=fd.get("czyDotacjaWPrzyszlymRoku"),
        partner_universities=fd.get("opiekaDydaktycznoNaukowaUczelni"),
        voivodeship=fd.get("wojewodztwo"),
        voivodeship_code=fd.get("wojewodztwoKodTERYT"),
        county=fd.get("powiat"),
        county_code=fd.get("powiatKodTERYT"),
        borough=fd.get("gmina"),
        borough_code=fd.get("gminaKodTERYT"),
        city=fd.get("miejscowosc"),
        city_code=fd.get("miejscowoscKodTERYT"),
        street=fd.get("ulica"),
        street_code=fd.get("ulicaKodTERYT"),
        building_number=fd.get("numerBudynku"),
        apartment_number=fd.get("numerLokalu"),
        postal_code=fd.get("kodPocztowy"),
        latitude=fd.get("geolokalizacja", {}).get("latitude"),
        longitude=fd.get("geolokalizacja", {}).get("longitude"),
        phone=fd.get("telefon"),
        email=fd.get("email"),
        website=fd.get("stronaInternetowa"),
    )
    return rspo_institution
