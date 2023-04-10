from re import sub
from typing import Generic, TypeVar

from fastapi import Query
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.default import Params as BaseParams
from pydantic import BaseModel


def camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


class CamelCasedModel(BaseModel):
    class Config:
        alias_generator = camel_case
        allow_population_by_field_name = True


def camel_case_model(model):
    class MyModel(model, CamelCasedModel):
        pass

    return MyModel


T = TypeVar("T")


class MaxPaginationLimitParams(BaseParams):
    size: int = Query(1_000, ge=1, le=1_000, description="Page size")


class MaxPaginationLimitPage(BasePage[T], Generic[T]):
    __params_type__ = MaxPaginationLimitParams
