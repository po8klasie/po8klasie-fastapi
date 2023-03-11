from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from po8klasie_fastapi.db.db import get_db
from po8klasie_fastapi.app.project.models import Project

project_router = APIRouter()


class ProjectSchema(BaseModel):
    project_id: str
    project_name: str

    class Config:
        orm_mode = True


@project_router.get("/", response_model=List[ProjectSchema])
async def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@project_router.get("/{project_id}", response_model=ProjectSchema)
async def get_single_project(project_id: str = None, db: Session = Depends(get_db)):
    return db.query(Project).filter_by(project_id=project_id).one()
