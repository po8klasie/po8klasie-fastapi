from sqlalchemy import Column
from sqlalchemy.types import String
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String, primary_key=True)
    project_name = Column(String)
