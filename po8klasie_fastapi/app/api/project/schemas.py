from enum import Enum
from typing import Optional

from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel
from po8klasie_fastapi.app.project.schemas import (
    SchoolViewConfigSchema,
    SearchViewConfigSchema,
)


class ProjectSelectablePropertiesEnum(Enum):
    project_name = "project_name"
    school_view_config = "school_view_config"
    search_view_config = "search_view_config"


class ProjectResponseSchema(CamelCasedModel):
    project_id: str
    project_name: Optional[str]

    school_view_config: Optional[SchoolViewConfigSchema]
    search_view_config: Optional[SearchViewConfigSchema]

    class Config:
        orm_mode = True
