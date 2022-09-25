from sqlalchemy.orm import Session

from app.rspo_institution.models import RspoInstitution
from db.models import Institution


def remove_institutions_outside_project_boundaries(db: Session):
    institution_to_remove = (
        db.query(Institution)
        .join(RspoInstitution)
        .filter(RspoInstitution.name == "I LICEUM W CHMURZE")
        .one()
    )

    db.delete(institution_to_remove)


patches_list = [remove_institutions_outside_project_boundaries]


def apply_data_patches(db: Session):
    for patch_fn in patches_list:
        patch_fn(db)
