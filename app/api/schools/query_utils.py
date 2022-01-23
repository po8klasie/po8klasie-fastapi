from sqlalchemy.orm import Session

from app.data_providers.rspo_api.models import RspoFacility


def query_rspo_facility(db: Session):
    return db.query(RspoFacility).filter(
        RspoFacility.students_category.has(name="Dzieci lub młodzież")
    )


def get_schools(db: Session, project_id: str):
    query = query_rspo_facility(db)
    if project_id:
        query = query.filter_by(project_id=project_id)
    return query


def get_school(db: Session, rspo: str):
    return query_rspo_facility(db).filter_by(rspo=rspo).one()
