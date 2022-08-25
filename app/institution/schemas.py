from typing import Optional, List

from app.lib.router_utils import CamelCasedModel


class InstitutionListItemSchema(CamelCasedModel):
    project_id: Optional[str]
    name: str
    rspo: str
    rspo_institution_type: int
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


class InstitutionResponseSchema(InstitutionListItemSchema):
    email: str
    phone: str
    website: str
    postal_code: str
    description: Optional[str]
