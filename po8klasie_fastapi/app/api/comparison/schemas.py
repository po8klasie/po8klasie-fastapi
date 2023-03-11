from __future__ import annotations

from typing import List

from po8klasie_fastapi.app.api.comparison.comparison_utils import ComparisonResultEnum
from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel


class ComparisonItemSchema(CamelCasedModel):
    value: int | str
    comparison_result: ComparisonResultEnum


class ComparisonItemsSchema(CamelCasedModel):
    is_public: ComparisonItemSchema
    city: ComparisonItemSchema
    available_languages: List[ComparisonItemSchema]
    classes: List[ComparisonItemSchema]


class ComparisonInstitutionSchema(CamelCasedModel):
    name: str
    rspo: str
    comparison: ComparisonItemsSchema