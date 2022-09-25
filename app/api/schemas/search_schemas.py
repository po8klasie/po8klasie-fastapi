from typing import Optional, List

from app.institution.models import InstitutionTypeGeneralizedEnum
from app.lib.router_utils import CamelCasedModel


class SearchListItemSchema(CamelCasedModel):
    project_id: Optional[str]
    name: str
    institution_type_generalized: InstitutionTypeGeneralizedEnum
    rspo: str
    street: str
    building_number: str
    apartment_number: str
    city: str

    is_public: bool

    latitude: float
    longitude: float

    borough: str
    city: str

    foreign_languages: Optional[List[str]]
    class_profiles: Optional[List[str]]

    class Config:
        orm_mode = True
