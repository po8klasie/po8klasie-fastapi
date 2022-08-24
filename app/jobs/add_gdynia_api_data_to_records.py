from app.db.db import get_db
from app.models.facility import Facility
from app.providers.gdynia_api.fetch import fetch_gdynia_facility_data
from app.providers.gdynia_api.model_mapper import add_gdynia_facility_data_to_model


def add_gdynia_api_data_to_records():
    db = next(get_db())

    gdynia_facility_data = fetch_gdynia_facility_data()

    for gdynia_single_facility_data in gdynia_facility_data:
        rspo = gdynia_single_facility_data.get("rspo")

        facility_match = db.query(Facility).filter_by(rspo=rspo).first()

        if not facility_match:
            continue

        facility_match = add_gdynia_facility_data_to_model(
            facility_match, gdynia_single_facility_data
        )
        db.add(facility_match)

    db.commit()
