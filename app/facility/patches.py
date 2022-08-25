from sqlalchemy.orm import Session

from app.facility.models import Facility
from app.lib.yaml_utils import parse_yaml_file

patches_file = "./app/facility/data_patches/patches.yml"


def apply_data_patches(db: Session):
    patches = parse_yaml_file(patches_file)["patches"]
    if patches:
        for patch in patches:
            facility = db.query(Facility).filter_by(**patch["where"]).one()
            if "update" in patch:
                for key, value in patch["update"].items():
                    setattr(facility, key, value)
