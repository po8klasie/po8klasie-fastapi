from sqlalchemy import desc, func
from sqlalchemy.orm import Query as SQLAlchemyQuery

from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution


def order_institutions(institutions: SQLAlchemyQuery) -> SQLAlchemyQuery:
    return institutions.order_by(
        func.array_length(SecondarySchoolInstitution.available_extended_subjects, 1)
        == 0,
        desc(
            func.array_length(SecondarySchoolInstitution.available_extended_subjects, 1)
        ),
    )
