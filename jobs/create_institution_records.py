from requests import Session

from db.db import get_db
from app.institution.providers.rspo_api.model_mapper import (
    create_model_from_institution_data,
)
from app.institution.providers.rspo_api.fetch import fetch_borough_institution_data


def create_borough_institution_records(db: Session, borough_name: str, project_id: str):
    for institution_data in fetch_borough_institution_data(borough_name):
        db.add(
            create_model_from_institution_data(
                db=db, fd=institution_data, project_id=project_id
            )
        )


def create_institution_records():
    db = next(get_db())

    create_borough_institution_records(db, "warszawa", "warszawa")
    create_borough_institution_records(db, "gdynia", "gdynia")
    db.commit()
