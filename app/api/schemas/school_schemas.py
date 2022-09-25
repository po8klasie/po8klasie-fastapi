from typing import Optional

from app.api.schemas.search_schemas import SearchListItemSchema


class SingleSchoolResponseSchema(SearchListItemSchema):
    email: str
    phone: str
    website: str
    postal_code: str
    description: Optional[str]
