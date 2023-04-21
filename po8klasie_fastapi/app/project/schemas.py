from typing import Any, Dict, List

from pydantic import BaseModel, validator


class DefaultMapViewSchema(BaseModel):
    center: List[float]
    zoom: float

    @validator("center")
    def check_len_eq_2(cls, value):
        if len(value) != 2:
            raise ValueError("map_options.center should have len == 2")
        return value


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
