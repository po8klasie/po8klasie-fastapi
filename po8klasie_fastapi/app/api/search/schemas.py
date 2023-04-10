from typing import Optional, List

from po8klasie_fastapi.app.institution.models import InstitutionTypeGeneralizedEnum
from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel


class InstitutionClass(CamelCasedModel):
    class_name: str

    class Config:
        orm_mode = True


class SecondarySchoolInstitutionSchema(CamelCasedModel):
    project_id: str
    institution_type_generalized: InstitutionTypeGeneralizedEnum

    available_languages: List[str]

    class Config:
        orm_mode = True


class RspoInstitutionSchema(CamelCasedModel):
    name: str
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

    class Config:
        orm_mode = True


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

    classes: List[InstitutionClass]

    class Config:
        orm_mode = True
