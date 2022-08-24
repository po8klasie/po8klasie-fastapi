from requests import Session

from app.db.db import get_db
from app.providers.rspo_api.model_mapper import create_model_from_facility_data
from app.providers.rspo_api.fetch import fetch_borough_facility_data


def create_borough_facility_records(db: Session, borough_name: str, project_id: str):
    for facility_data in fetch_borough_facility_data(borough_name):
        db.add(
            create_model_from_facility_data(
                db=db, fd=facility_data, project_id=project_id
            )
        )


def create_facility_records():
    db = next(get_db())

    create_borough_facility_records(db, "warszawa", "warszawa")
    create_borough_facility_records(db, "gdynia", "gdynia")
    db.commit()
