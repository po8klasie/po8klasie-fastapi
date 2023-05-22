from dataclasses import dataclass

from po8klasie_fastapi.app.api.comparison.schemas import (
    ComparisonInstitutionDataSchema,
    ComparisonComparableDataSchema,
    ComparisonResultEnum,
    ComparisonInstitution,
)


@dataclass
class ComparisonInternalStateItem:
    institution_data: ComparisonInstitutionDataSchema
    comparable_data: ComparisonComparableDataSchema


def create_comparison_internal_state(institutions_to_compare):
    for institution in institutions_to_compare:
        parsed_institution_data = ComparisonInstitutionDataSchema.parse_institution(
            institution
        )
        parsed_comparable_data = ComparisonComparableDataSchema.parse_institution(
            institution
        )
        yield ComparisonInternalStateItem(
            institution_data=parsed_institution_data,
            comparable_data=parsed_comparable_data,
        )


def compare(institutions_to_compare):
    internal_comparison_state = list(
        create_comparison_internal_state(institutions_to_compare)
    )
    comparable_fields = ComparisonComparableDataSchema.__fields__.keys()

    def get_field_value(comparison_state_item, field_name):
        value = getattr(comparison_state_item.comparable_data, field_name)
        if isinstance(value, list):
            return tuple(value)
        return value

    all_fields_values = {
        field: set(
            get_field_value(comparison_state_item, field)
            for comparison_state_item in internal_comparison_state
        )
        for field in comparable_fields
    }

    def get_single_field_comparison_result(field_name):
        is_field_value_common = len(all_fields_values[field_name]) == 1
        if is_field_value_common:
            return ComparisonResultEnum.MATCH
        return ComparisonResultEnum.NEUTRAL

    def get_single_field_comparison(field_name, comparison_institution):
        return {
            "value": getattr(
                comparison_institution.comparable_data, field_name
            ),
            "comparison_result": get_single_field_comparison_result(field_name),
        }

    def get_iterable_field_comparison(field_name, comparison_institution):
        for item in getattr(comparison_institution.comparable_data, field_name):
            set_of_all_lists = all_fields_values[field_name]
            is_item_in_all_lists = all(item in list_for_field for list_for_field in set_of_all_lists)

            yield {
                "value": item,
                "comparison_result": ComparisonResultEnum.MATCH if is_item_in_all_lists else ComparisonResultEnum.NEUTRAL,
            }

    def is_field_iterable(field_name, comparison_institution):
        value = getattr(comparison_institution.comparable_data, field_name)
        return isinstance(value, list)

    for comparison_state_institution in internal_comparison_state:
        yield ComparisonInstitution(
            comparison={
                field: (
                    list(get_iterable_field_comparison(field, comparison_state_institution))
                    if is_field_iterable(field, comparison_state_institution)
                    else get_single_field_comparison(field, comparison_state_institution)
                )
                for field in comparable_fields
            },
            **comparison_state_institution.institution_data.dict()
        )
