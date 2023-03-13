from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.types import String
from po8klasie_fastapi.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String, primary_key=True)
    project_name = Column(String)
    school_view_config = Column(JSON)
    search_view_config = Column(JSON)
