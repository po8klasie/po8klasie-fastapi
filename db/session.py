from sqlalchemy.orm import sessionmaker

from db.db import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
