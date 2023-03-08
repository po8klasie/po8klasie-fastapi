from __future__ import annotations

from typing import List, Any

from app.api.search.schemas import SearchListItemSchema


class SingleInstitutionResponseSchema(SearchListItemSchema):
    postal_code: str
    email: str
    phone: str
    website: str
    description: str | None
    # education offer section
    extracurricular_activities: List[str] | None
    school_events: List[str] | None
    no_of_school_trips_per_year: str | None
    # sport section
    sport_activities: List[str] | None
    sport_infrastructure: List[str] | None
    # partners section
    NGO_partners: List[str] | None
    university_partners: List[str] | None
    # students stats section
    avg_students_no_per_class: int | None
    min_students_no_per_class: int | None
    max_students_no_per_class: int | None
    no_of_students_taking_part_in_olympiads: str | None
    # student support section
    no_of_fulltime_psychologist_positions: float | None

    classes: Any
    public_transport_stops: Any
