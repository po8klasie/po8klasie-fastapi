from app.institution.patches import apply_data_patches as apply
from db.db import get_db


def apply_data_patches():
    db = next(get_db())
    apply(db)
    db.commit()
