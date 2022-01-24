from typing import Dict

from sqlalchemy.orm import Session


from app.db.db_utils import get_or_create
from app.models import (
    Project,
    RspoEntityType,
    RspoFacilityLegalStatus,
    RspoStudentsCategory,
    RspoReportingEntity,
    RspoFacilityOwnerEntity,
    RspoFacility,
    RspoFacilityBindingType,
)


def create_subfield_mapping_model(db, Model, data):
    return get_or_create(
        model=Model, session=db, id=data.get("id"), name=data.get("nazwa")
    )[0]


def create_model_from_reporting_entity_data(db, data):
    reporting_entity, is_new = get_or_create(
        model=RspoReportingEntity,
        session=db,
        name=data.get("nazwa"),
        regon=data.get("regon"),
    )
    reporting_entity.entity_type = create_subfield_mapping_model(
        db, RspoEntityType, data.get("typ")
    )
    return reporting_entity


def create_model_from_owner_entity_data(db, data):
    owner_entity, is_new = get_or_create(
        model=RspoFacilityOwnerEntity,
        session=db,
        id=data.get("id"),
        name=data.get("nazwa"),
        regon=data.get("regon"),
    )
    owner_entity.entity_type = create_subfield_mapping_model(
        db, RspoEntityType, data.get("typ")
    )
    return owner_entity


def create_model_from_facility_data(db: Session, fd: Dict, project_id: str):
    facility = RspoFacility(
        project=db.query(Project).filter_by(project_id=project_id).one(),
        rspo=fd.get("numerRspo"),
        foundation_date=fd.get("dataZalozenia"),
        commencement_date=fd.get("dataRozpoczecia"),
        shutdown_date=fd.get("dataZakonczenia"),
        termination_date=fd.get("dataLikwidacji"),
        complex_inclusion_date=fd.get("dataWlaczeniaDoZespolu"),
        complex_exclusion_date=fd.get("dataWylaczeniaZZespolu"),
        nip=fd.get("nip"),
        regon=fd.get("regon"),
        name=fd.get("nazwa"),
        shortened_name=fd.get("nazwaSkrocona"),
        facility_type=create_subfield_mapping_model(db, RspoEntityType, fd.get("typ")),
        principal_first_name=fd.get("dyrektorImie"),
        principal_last_name=fd.get("dyrektorNazwisko"),
        facility_legal_status=create_subfield_mapping_model(
            db, RspoFacilityLegalStatus, fd.get("statusPublicznoPrawny")
        ),
        students_category=create_subfield_mapping_model(
            db, RspoStudentsCategory, fd.get("kategoriaUczniow")
        ),
        school_specifics=fd.get("specyfikaSzkoly"),
        facility_binding_type=create_subfield_mapping_model(
            db, RspoFacilityBindingType, fd.get("zwiazanieOrganizacyjne")
        ),
        has_school_area=fd.get("czyPosiadaObwod"),
        has_dormitory=fd.get("czyPosiadaInternat"),
        next_year_subsidy=fd.get("czyDotacjaWPrzyszlymRoku"),
        partner_universities=fd.get("opiekaDydaktycznoNaukowaUczelni"),
        reporting_entity=create_model_from_reporting_entity_data(
            db, fd.get("podmiotPrzekazujacyDaneDoRSPO")
        ),
        facility_owner_entity=create_model_from_owner_entity_data(
            db, fd.get("podmiotProwadzacy")
        ),
        parent_entity=fd.get("podmiotNadrzedny"),
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
        forwarding_address_city=fd.get("adresDoKorespondecjiMiejscowosc"),
        forwarding_address_street=fd.get("adresDoKorespondecjiUlica"),
        forwarding_address_building_no=fd.get("adresDoKorespondecjiNumerBudynku"),
        forwarding_address_apartment_no=fd.get("adresDoKorespondecjiNumerLokalu"),
        forwarding_address_postal_code=fd.get("adresDoKorespondecjiKodPocztowy"),
        dependent_facilities=fd.get("placowkiPodrzedne"),
    )
    return facility
