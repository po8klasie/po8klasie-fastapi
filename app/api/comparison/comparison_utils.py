from __future__ import annotations

from enum import Enum
from typing import TypedDict, List


class ComparisonResultEnum(Enum):
    MATCH = "match"
    NEUTRAL = "neutral"


class ComparisonItemT(TypedDict):
    value: int | str
    comparison_result: ComparisonResultEnum


def is_iterable(x) -> bool:
    try:
        iter(x)
        return not isinstance(x, str)
    except TypeError:
        return False


def find_intersection(institutions, property_key=None, getter_fn=None) -> set:
    def get_single_set(idx):
        value = None
        if not property_key and not getter_fn:
            raise Exception("No property key nor getter function specified")

        if property_key:
            institution = institutions[idx]
            value = getattr(institution, property_key)
        if getter_fn:
            value = getter_fn(institutions[idx].rspo)

        if is_iterable(value):
            return set(value)
        return {value}

    intersection = None
    for i in range(len(institutions)):
        if i == 0:
            intersection = get_single_set(i)
        intersection = intersection.intersection(get_single_set(i))
    return intersection


def get_comparison_result(is_in_intersection) -> ComparisonResultEnum:
    if is_in_intersection:
        return ComparisonResultEnum.MATCH
    return ComparisonResultEnum.NEUTRAL


def get_comparison_item(value, intersection) -> ComparisonItemT | List[ComparisonItemT]:
    if not is_iterable(value):
        return {
            "value": value,
            "comparison_result": get_comparison_result(value in intersection),
        }

    return [
        {
            "value": value_item,
            "comparison_result": get_comparison_result(value_item in intersection),
        }
        for value_item in value
    ]
