import itertools
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from po8klasie_fastapi.app.api.institution.schemas import (
    SingleInstitutionResponseSchema,
)
from po8klasie_fastapi.app.api.search.filtering import (
    search_router_secondary_school_entities,
)
from po8klasie_fastapi.app.institution.models import (
    SecondarySchoolInstitution,
    query_secondary_school_institutions,
)
from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
    query_current_classes,
)
from po8klasie_fastapi.app.public_transport_info.models import (
    InstitutionPublicTransportStopAssociation,
)
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution
from po8klasie_fastapi.db.db import get_db

school_router = APIRouter()

school_router_secondary_school_entities = [
    *search_router_secondary_school_entities,
    RspoInstitution.postal_code,
    RspoInstitution.email,
    RspoInstitution.phone,
    RspoInstitution.website,
    SecondarySchoolInstitution.description,
    # education offer section
    SecondarySchoolInstitution.extracurricular_activities,
    SecondarySchoolInstitution.school_events,
    SecondarySchoolInstitution.no_of_school_trips_per_year,
    # sport section
    SecondarySchoolInstitution.sport_activities,
    SecondarySchoolInstitution.sport_infrastructure,
    # partners section
    SecondarySchoolInstitution.NGO_partners,
    SecondarySchoolInstitution.university_partners,
    # students stats section
    SecondarySchoolInstitution.avg_students_no_per_class,
    SecondarySchoolInstitution.min_students_no_per_class,
    SecondarySchoolInstitution.max_students_no_per_class,
    SecondarySchoolInstitution.no_of_students_taking_part_in_olympiads,
    # student support section
    SecondarySchoolInstitution.no_of_fulltime_psychologist_positions,
]


@school_router.get("/", response_model=List[SingleInstitutionResponseSchema])
def route_get_schools(db: Session = Depends(get_db)):
    return query_secondary_school_institutions(
        db, school_router_secondary_school_entities
    ).all()


@school_router.get("/multiple")
def route_comparison(
    rspo: List[str] = Query(default=[]), db: Session = Depends(get_db)
):
    if len(rspo) == 0:
        raise HTTPException(status_code=422, detail="No rspos provided")

    try:
        institutions = (
            query_secondary_school_institutions(
                db, school_router_secondary_school_entities
            )
            .filter(SecondarySchoolInstitution.rspo.in_(rspo))
            .all()
        )

        for institution in institutions:
            classes = (
                query_current_classes(db)
                .with_entities(
                    SecondarySchoolInstitutionClass.extended_subjects,
                    SecondarySchoolInstitutionClass.class_name,
                )
                .filter(
                    SecondarySchoolInstitutionClass.institution_rspo == institution.rspo
                )
                .all()
            )
            yield {**dict(institution), "classes": classes}

    except NoResultFound:
        raise HTTPException(status_code=404, detail="No schools found")


@school_router.get("/{rspo}", response_model=SingleInstitutionResponseSchema)
def route_get_single_school(rspo: str, db: Session = Depends(get_db)):
    try:
        institution = (
            query_secondary_school_institutions(
                db, school_router_secondary_school_entities
            )
            .filter_by(rspo=rspo)
            .one()
        )

        classes_list = (
            db.query(SecondarySchoolInstitutionClass)
            .filter(
                SecondarySchoolInstitutionClass.institution_rspo == institution.rspo
            )
            .order_by(SecondarySchoolInstitutionClass.year)
            .all()
        )

        classes = {
            k: list(g) for k, g in itertools.groupby(classes_list, lambda c: c.year)
        }

        public_transport_stops = (
            db.query(InstitutionPublicTransportStopAssociation)
            .filter_by(institution_rspo=rspo)
            .all()
        )

        return {
            **dict(institution),
            "classes": classes,
            "public_transport_stops": public_transport_stops,
        }

    except NoResultFound:
        raise HTTPException(status_code=404, detail="No school found")
