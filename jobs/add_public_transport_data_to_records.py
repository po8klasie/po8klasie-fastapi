from app.public_transport_info.model_mapper import (
    add_public_transport_stops_data_to_institution,
)
from cli.cli_logger import cli_logger
from db.db import get_db
from app.institution.models import Institution

import db.models

STOP_DISTANCE_FROM_INSTITUTION = 250


def add_public_transport_data_to_records():
    db = next(get_db())

    institutions = db.query(Institution)

    count = len(institutions)
    i = 0

    for institution in institutions:
        i += 1
        cli_logger.info(
            f"{i}/{count}. Adding public transport data for institution #{institution.rspo}"
        )
        has_not_succeeded = True

        while has_not_succeeded:
            try:
                add_public_transport_stops_data_to_institution(
                    db=db,
                    institution=institution,
                    distance=STOP_DISTANCE_FROM_INSTITUTION,
                )
                db.add(institution)
                has_not_succeeded = False
            except Exception as e:
                print(e)
                print("Error occurred. Retrying")

    db.commit()
