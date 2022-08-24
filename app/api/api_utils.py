from re import sub
from typing import TypeVar, Generic

from fastapi import Query
from pydantic import BaseModel
from fastapi_pagination.default import Page as BasePage, Params as BaseParams


def camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


class CamelCasedModel(BaseModel):
    class Config:
        alias_generator = camel_case
        allow_population_by_field_name = True


T = TypeVar("T")


class MaxPaginationLimitParams(BaseParams):
    size: int = Query(1_000, ge=1, le=1_000, description="Page size")


class MaxPaginationLimitPage(BasePage[T], Generic[T]):
    __params_type__ = MaxPaginationLimitParams
