from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.projects.models import Project

projects_router = APIRouter()


class ProjectSchema(BaseModel):
    project_id: str
    project_name: str

    class Config:
        orm_mode = True


@projects_router.get("/", response_model=List[ProjectSchema])
async def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@projects_router.get("/{project_id}", response_model=ProjectSchema)
async def get_single_project(project_id: str = None, db: Session = Depends(get_db)):
    return db.query(Project).filter_by(project_id=project_id).one()
