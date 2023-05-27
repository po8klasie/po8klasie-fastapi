import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from po8klasie_fastapi.app.rankings.zwzt.consts import ZWZT_LATEST_RANKING_EDITION_YEAR
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution
from po8klasie_fastapi.db.base import Base


class ZwzTRankingEntry(Base):
    __tablename__ = "zwzt_ranking_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    year = Column(Integer)

    place_in_country = Column(Integer)
    place_in_voivodeship = Column(Integer)

    indicator_value = Column(Float)

    institution_rspo = Column(String, ForeignKey("secondary_school_institutions.rspo"))
    institution = relationship("SecondarySchoolInstitution", back_populates="zwzt_ranking_entries")


zwzt_ranking_entries_base_filters = [
    RspoInstitution.rspo == ZwzTRankingEntry.institution_rspo,
    ZwzTRankingEntry.year == ZWZT_LATEST_RANKING_EDITION_YEAR,
]