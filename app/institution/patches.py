from sqlalchemy.orm import Session

from app.institution.models import Institution
from app.lib.yaml_utils import parse_yaml_file

patches_file = "./app/institution/data_patches/patches.yml"


def apply_data_patches(db: Session):
    patches = parse_yaml_file(patches_file)["patches"]
    if patches:
        for patch in patches:
            institution = db.query(Institution).filter_by(**patch["where"]).one()
            if "update" in patch:
                for key, value in patch["update"].items():
                    setattr(institution, key, value)
