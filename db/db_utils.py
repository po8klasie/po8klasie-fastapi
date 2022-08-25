# https://stackoverflow.com/a/2587041
from sqlalchemy import MetaData
from sqlalchemy.sql import ClauseElement

from db.base import Base
from db.db import engine


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
        params.update(defaults or {})
        instance = model(**params)
        try:
            session.add(instance)
            session.commit()
        # The actual exception depends on the specific database so we catch all exceptions.
        # This is similar to the official documentation:
        # https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
        except Exception:
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance, False
        else:
            return instance, True


def drop_all():
    meta = MetaData(bind=engine)
    meta.reflect()

    for tbl in reversed(meta.sorted_tables):
        engine.execute(tbl.delete())


def create_all():
    Base.metadata.create_all(bind=engine)
