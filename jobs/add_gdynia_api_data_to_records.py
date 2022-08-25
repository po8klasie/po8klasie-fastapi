from db.db import get_db
from app.institution.models import Institution
from app.institution.providers.gdynia_api.fetch import fetch_gdynia_institution_data
from app.institution.providers.gdynia_api.model_mapper import (
    add_gdynia_institution_data_to_model,
)


def add_gdynia_api_data_to_records():
    db = next(get_db())

    gdynia_institution_data = fetch_gdynia_institution_data()

    for gdynia_single_institution_data in gdynia_institution_data:
        rspo = gdynia_single_institution_data.get("rspo")

        institution_match = db.query(Institution).filter_by(rspo=rspo).first()

        if not institution_match:
            continue

        institution_match = add_gdynia_institution_data_to_model(
            institution_match, gdynia_single_institution_data
        )
        db.add(institution_match)

    db.commit()
