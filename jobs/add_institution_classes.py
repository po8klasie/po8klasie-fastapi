import csv

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.institution.models import SecondarySchoolInstitution
from app.institution_classes.models import SecondarySchoolInstitutionClass
from app.rspo_institution.models import RspoInstitution
from db.db import get_db


def add_institution_classes():
    db: Session = next(get_db())

    with open("./data/institution_classes/warszawa_classes.csv") as f:
        reader = csv.DictReader(f, delimiter=";")
        skipped_school_names = []
        n = 0

        for row in reader:
            school_name = row["school_name"]

            try:
                institution_match = (
                    db.query(SecondarySchoolInstitution)
                    .join(RspoInstitution)
                    .filter(func.lower(RspoInstitution.name) == school_name.lower())
                    .one()
                )

                available_languages = row["available_languages"].split(",")
                extended_subjects = row["extended_subjects"].split(",")
                points_stats_min = float(row["points_stats_min"].replace(",", "."))

                if row["year"] == "2022":
                    institution_match.available_languages = list(
                        {*institution_match.available_languages, *available_languages}
                    )
                    institution_match.available_extended_subjects = list(
                        {
                            *institution_match.available_extended_subjects,
                            *extended_subjects,
                        }
                    )
                    if points_stats_min and points_stats_min > 0:
                        institution_match.points_stats_min = min(
                            points_stats_min,
                            institution_match.points_stats_min
                            if institution_match.points_stats_min
                            else 1000,
                        )
                        print(points_stats_min)

                institution_class = SecondarySchoolInstitutionClass(
                    institution=institution_match,
                    year=row["year"],
                    class_name=row["class_name"],
                    class_symbol=row["class_symbol"],
                    class_type=row["class_type"],
                    class_size=row["class_size"],
                    occupation=row["occupation"],
                    available_languages=available_languages,
                    extended_subjects=extended_subjects,
                    points_stats_min=points_stats_min,
                    points_stats_avg=float(row["points_stats_avg"].replace(",", ".")),
                    points_stats_max=float(row["points_stats_max"].replace(",", ".")),
                )

                n += 1
                db.add(institution_class)
                db.add(institution_match)

            except Exception as e:
                if school_name not in skipped_school_names:
                    skipped_school_names.append(school_name)
                    print(f"Skipping {school_name}: {e}")
                    continue

        db.commit()
        print(f"Added {n} records. Skipped {len(skipped_school_names)}.")
