from po8klasie_fastapi.app.api.schemas import InstitutionSourcingSchemaMixin
from po8klasie_fastapi.app.lib.router_utils import CamelCasedModel


class SearchAutocompleteItemSchema(CamelCasedModel, InstitutionSourcingSchemaMixin):
    project_id: str
    rspo: str
    name: str
