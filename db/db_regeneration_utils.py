# flake8: noqa
from sqlalchemy import MetaData

from db.base import Base
from db.db import engine

# import all known models
import app.institution.models
import app.project.models


def drop_all():
    meta = MetaData(bind=engine)
    meta.reflect()

    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())


def create_all():
    Base.metadata.create_all(engine)
