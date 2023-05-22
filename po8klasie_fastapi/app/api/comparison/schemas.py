from enum import Enum

from pydantic import validator, create_model, Field
from typing import Any

from po8klasie_fastapi.app.api.schemas import InstitutionSourcingSchemaMixin
from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel


class ComparisonInstitutionDataSchema(CamelCasedModel, InstitutionSourcingSchemaMixin):
    rspo: str
    name: str


class ComparisonComparableDataSchema(CamelCasedModel, InstitutionSourcingSchemaMixin):
    is_public: bool
    city: str
    available_languages: list[str]
    classes: list[str]

    @validator("classes", pre=True)
    def preprocess_classes(cls, classes):
        return ["-".join(class_.extended_subjects) for class_ in classes]


class ComparisonResultEnum(Enum):
    MATCH = "match"
    NEUTRAL = "neutral"


class ComparisonField(CamelCasedModel):
    value: Any
    comparison_result: ComparisonResultEnum


ComparisonInstitutionResultSnakeCase = create_model(
    "ComparisonInstitutionResult",
    **{
        field_name: (ComparisonField | list[ComparisonField], Field(title=field_name))
        for field_name in ComparisonComparableDataSchema.__fields__.keys()
    }
)


class ComparisonInstitutionResult(
    ComparisonInstitutionResultSnakeCase, CamelCasedModel
):
    pass


class ComparisonInstitution(ComparisonInstitutionDataSchema):
    comparison: ComparisonInstitutionResult
