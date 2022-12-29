import shapely.geometry

from app.institution.models import SecondarySchoolInstitution
from app.rspo_institution.fetch import fetch_borough_rspo_institution_data
from app.rspo_institution.model_mapper import create_model_from_rspo_institution_data
from db.db import get_db


def create_borough_institution_records(db, borough_name: str, project_id: str):
    for institution_data in fetch_borough_rspo_institution_data(borough_name):
        institution = SecondarySchoolInstitution(
            rspo_institution=create_model_from_rspo_institution_data(institution_data),
            available_languages=[],
            available_extended_subjects=[],
            points_stats_max=1000,
            points_stats_min=-1,
            project_id=project_id,
        )

        institution.geometry = shapely.geometry.Point(
            map(
                float,
                (
                    institution.rspo_institution.longitude,
                    institution.rspo_institution.latitude,
                ),
            )
        ).wkt

        db.add(institution)


def create_institution_records():
    db = next(get_db())

    create_borough_institution_records(db, "warszawa", "warszawa")
    create_borough_institution_records(db, "gdynia", "gdynia")
    db.commit()
