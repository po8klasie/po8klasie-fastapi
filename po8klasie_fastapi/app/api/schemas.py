from pydantic import BaseModel
from typing import List

from po8klasie_fastapi.app.institution.models import (
    InstitutionTypeGeneralizedEnum,
    SecondarySchoolInstitution,
)
from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution


class InstitutionSourcingSchemaMixin(BaseModel):
    @classmethod
    def parse_institution(cls, institution: SecondarySchoolInstitution):
        rspo_institution_columns = RspoInstitution.__table__.columns.keys()
        schema_fields = cls.__fields__.keys()

        obj = dict()

        for field in schema_fields:
            if field in rspo_institution_columns:
                obj[field] = getattr(institution.rspo_institution, field)
            else:
                obj[field] = getattr(institution, field)

        return cls.parse_obj(obj)


class InstitutionOverviewInstitutionClassSchema(CamelCasedModel):
    extended_subjects: list[str]

    class Config:
        orm_mode = True


class InstitutionOverviewSchema(
    CamelCasedModel,
    InstitutionSourcingSchemaMixin,
):
    rspo: str
    project_id: str

    name: str

    is_public: bool
    rspo_institution_type: str
    institution_type_generalized: InstitutionTypeGeneralizedEnum

    city: str
    street: str
    borough: str
    building_number: str
    apartment_number: str

    latitude: float
    longitude: float

    available_languages: List[str]
    classes: list[InstitutionOverviewInstitutionClassSchema]

    points_stats_min: float | None

    class Config:
        orm_mode = True
