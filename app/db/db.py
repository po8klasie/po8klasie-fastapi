from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.db_url)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    yield db
