import unittest
from random import randint

import factory
import faker
from faker_education import SchoolProvider
from fastapi.testclient import TestClient as FastApiTestClient

from po8klasie_fastapi.app.config import settings

from po8klasie_fastapi.db.db import get_db
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

if not settings.test_db_url:
    raise KeyError("TEST_DATABASE_URL not specified")

engine = create_engine(settings.test_db_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingScopedSession = scoped_session(TestingSessionLocal)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def get_test_db():
    return next(override_get_db())


class TestClient(FastApiTestClient):
    def __init__(self):
        from po8klasie_fastapi.app.main import app

        app.dependency_overrides[get_db] = override_get_db
        FastApiTestClient.__init__(self, app)


class TestingFixtures:
    @staticmethod
    def reset_db():
        meta = MetaData(bind=engine)
        meta.reflect()

        omit = ["spatial_ref_sys"]  # required by postgis

        for tbl in reversed(meta.sorted_tables):
            if str(tbl) not in omit:
                engine.execute(f"DROP TABLE IF EXISTS {tbl}")

        from po8klasie_fastapi.db.models import Base

        Base.metadata.reflect(bind=engine)
        Base.metadata.create_all(bind=engine)


fake = faker.Faker(
    locale="pl_PL", providers=["faker.providers.misc", "faker.providers.address"]
)
fake.add_provider(SchoolProvider)


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


def fake_rspo():
    return str(random_with_n_digits(9))


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = TestingScopedSession
        sqlalchemy_session_persistence = "commit"


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        TestingFixtures.reset_db()
        self.session = TestingScopedSession

    def tearDown(self):
        self.session.remove()


class ClientTestCase(DatabaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient()

    def tearDown(self):
        super().tearDown()
        self.client.close()
