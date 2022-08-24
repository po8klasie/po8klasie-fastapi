from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

connect_args = {
    # 'ssl': {
    #     'ssl_ca': 'https://cockroachlabs.cloud/clusters/8c62c158-8462-4f9e-998c-06afd6455fb6/cert'
    # }
}

engine = create_engine(settings.db_url, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    yield db
