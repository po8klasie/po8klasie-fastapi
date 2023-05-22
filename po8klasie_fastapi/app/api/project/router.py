from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.project.schemas import (
    ProjectResponseSchema,
    ProjectSelectablePropertiesEnum,
)
from po8klasie_fastapi.app.project.models import Project
from po8klasie_fastapi.app.project.schemas import ProjectSchema
from po8klasie_fastapi.db.db import get_db

project_router = APIRouter()


@project_router.get("/", response_model=List[ProjectSchema])
async def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@project_router.get("/{project_id}")
async def get_single_project(
    project_id: str = None,
    properties: list[ProjectSelectablePropertiesEnum] | None = Query(default=None),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter_by(project_id=project_id).one()
    required_columns = ["project_id", "project_name"]

    return ProjectResponseSchema.from_orm(project).dict(
        by_alias=True
    )
