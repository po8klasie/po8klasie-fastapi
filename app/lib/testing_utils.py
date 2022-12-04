from fastapi.testclient import TestClient as FastApiTestClient

from app.config import settings
from app.main import app

from db.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base

if not settings.test_db_url:
    raise KeyError("TEST_DB_URL not specified")

engine = create_engine(settings.test_db_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def get_test_db():
    return next(override_get_db())


class TestClient(FastApiTestClient):
    def __init__(self):
        FastApiTestClient.__init__(self, app)


class TestingFixtures:
    @staticmethod
    def reset_db():
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
