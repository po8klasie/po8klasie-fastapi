from typing import Any, Dict, List

from pydantic import BaseModel


class MapOptionsSchema(BaseModel):
    center: [float, float]
    zoom: float


class DefaultQuerySchema(BaseModel):
    project_id: str


class FilterConfigSchema(BaseModel):
    name: str
    component: str
    parser: str
    default_value: Any
    options: Dict[str, Any]


class SearchViewConfigSchema(BaseModel):
    map_options: MapOptionsSchema
    default_query: DefaultQuerySchema
    filters: List[FilterConfigSchema]


class SchoolInfoSectionConfigSchema(BaseModel):
    section_id: str
    options: Dict[str, Any]


class SchoolViewConfigSchema(BaseModel):
    school_info_sections: List[SchoolInfoSectionConfigSchema]


class ProjectSchema(BaseModel):
    project_id: str
    project_name: str

    school_view_config: SchoolViewConfigSchema
    search_view_config: SearchViewConfigSchema

    class Config:
        orm_mode = True
