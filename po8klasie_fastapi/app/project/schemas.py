from typing import Any, Dict, List

from pydantic import BaseModel


class DefaultMapViewSchema(BaseModel):
    latitude: float | int
    longitude: float | int
    zoom: float | int


class FilterConfigSchema(BaseModel):
    name: str
    component: str
    parser: str
    defaultValue: Any
    options: Dict[str, Any]


class SearchViewConfigSchema(BaseModel):
    defaultMapView: DefaultMapViewSchema
    filters: List[FilterConfigSchema]


class SchoolInfoSectionConfigSchema(BaseModel):
    sectionId: str
    options: Dict[str, Any]


class SchoolViewConfigSchema(BaseModel):
    schoolInfoSections: List[SchoolInfoSectionConfigSchema]


class ProjectSchema(BaseModel):
    project_id: str
    project_name: str

    school_view_config: SchoolViewConfigSchema
    search_view_config: SearchViewConfigSchema

    class Config:
        orm_mode = True
