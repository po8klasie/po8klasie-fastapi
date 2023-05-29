import itertools

from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Iterable

from po8klasie_fastapi.app.api.schemas import InstitutionSourcingSchemaMixin
from po8klasie_fastapi.app.institution.models import InstitutionTypeGeneralizedEnum
from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
)
from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel
from po8klasie_fastapi.app.public_transport_info.schemas import (
    InstitutionPublicTransportStopAssociationSchema,
)


class InstitutionDetailsBasicDataSchema(BaseModel):
    project_id: Optional[str]
    name: str
    institution_type_generalized: InstitutionTypeGeneralizedEnum
    rspo: str
    is_public: bool
    rspo_institution_type: str


class InstitutionDetailsOverviewSectionSchema(BaseModel):
    city: str
    postal_code: str
    street: str
    building_number: str
    apartment_number: str

    email: str
    phone: str
    website: str
    description: str | None

    latitude: float
    longitude: float


class InstitutionDetailsEducationOfferSectionSchema(BaseModel):
    extracurricular_activities: List[str] | None
    school_events: List[str] | None
    no_of_school_trips_per_year: str | None


class InstitutionDetailsSportsSectionSchema(BaseModel):
    sport_activities: List[str] | None
    sport_infrastructure: List[str] | None


class InstitutionDetailsPartnersSectionSchema(BaseModel):
    NGO_partners: List[str] | None
    university_partners: List[str] | None


class InstitutionDetailsClassProfileSchema(CamelCasedModel):
    class_symbol: str | None
    class_name: str | None
    class_type: str | None

    year: int

    extended_subjects: list[str]
    occupation: str | None
    available_languages: list[str]

    url: str | None

    points_stats_min: float | None
    points_stats_avg: float | None
    points_stats_max: float | None

    description: str | None

    class Config:
        orm_mode = True


class InstitutionDetailsClassProfilesSectionSchema(BaseModel):
    classes: Dict[int, List[InstitutionDetailsClassProfileSchema]]

    @validator("classes", pre=True)
    def group_classes_by_year(
            cls,
            classes: Iterable[SecondarySchoolInstitutionClass]
                     | dict[int, list[SecondarySchoolInstitutionClass]],
    ) -> dict[int, list[SecondarySchoolInstitutionClass]]:
        if isinstance(classes, dict):
            return classes

        def get_year(c):
            return c.year

        grouped_classes = {
            year: [
                InstitutionDetailsClassProfileSchema.from_orm(class_)
                for class_ in classes_per_year
            ]
            for year, classes_per_year in itertools.groupby(classes, get_year)
        }

        return grouped_classes


class ZwzTRankingEntrySchema(CamelCasedModel):
    year: int

    place_in_country: int
    place_in_voivodeship: int

    indicator_value: float

    class Config:
        orm_mode = True


class InstitutionDetailsZwzTSectionSchema(CamelCasedModel):
    zwzt_ranking_entries: List[ZwzTRankingEntrySchema]


class InstitutionDetailsPublicTransportSectionSchema(BaseModel):
    public_transport_stops: List[InstitutionPublicTransportStopAssociationSchema]


class InstitutionDetailsSchema(
    InstitutionDetailsBasicDataSchema,
    InstitutionDetailsOverviewSectionSchema,
    InstitutionDetailsEducationOfferSectionSchema,
    InstitutionDetailsClassProfilesSectionSchema,
    InstitutionDetailsSportsSectionSchema,
    InstitutionDetailsPartnersSectionSchema,
    InstitutionDetailsZwzTSectionSchema,
    InstitutionDetailsPublicTransportSectionSchema,
    CamelCasedModel,
    InstitutionSourcingSchemaMixin,
):
    class Config:
        orm_mode = True
