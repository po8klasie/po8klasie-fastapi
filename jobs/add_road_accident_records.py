import csv

from sqlalchemy.orm import Session

from db.models import RoadAccident
from db.db import get_db
import shapely.geometry


def add_road_accident_records():
    db: Session = next(get_db())

    with open("./data/sewik/accidents.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            accident = RoadAccident(
                sewik_id=row["sewik_id"],
                accident_type_id=row["accident_type_id"],
                geometry=shapely.geometry.Point(map(float, (row["x"], row["y"]))).wkt,
            )
            db.add(accident)
        db.commit()
