from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.lib.router_utils import camel_case_model
from po8klasie_fastapi.app.project.schemas import (
    ProjectSchema,
    SchoolViewConfigSchema,
    SearchViewConfigSchema,
)
from po8klasie_fastapi.db.db import get_db
from po8klasie_fastapi.app.project.models import Project

project_router = APIRouter()


@project_router.get("/", response_model=List[ProjectSchema])
async def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@project_router.get("/{project_id}", response_model=ProjectSchema)
async def get_single_project(project_id: str = None, db: Session = Depends(get_db)):
    return db.query(Project).filter_by(project_id=project_id).one()


@project_router.get(
    "/{project_id}/basic_info",
    response_model=camel_case_model(ProjectSchema),
    response_model_include={"project_id", "project_name"},
)
async def get_project_config_basic_info(
    project_id: str = None, db: Session = Depends(get_db)
):
    return db.query(Project).filter_by(project_id=project_id).one()


@project_router.get(
    "/{project_id}/school_view_config",
    response_model=camel_case_model(SchoolViewConfigSchema),
)
async def get_school_view_config(project_id: str = None, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(project_id=project_id).one()
    return project.school_view_config


@project_router.get(
    "/{project_id}/search_view_config",
    response_model=camel_case_model(SearchViewConfigSchema),
)
async def get_search_view_config(project_id: str = None, db: Session = Depends(get_db)):
    project = db.query(Project).filter_by(project_id=project_id).one()
    return project.search_view_config
