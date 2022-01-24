from typing import Dict

from sqlalchemy.orm import declarative_base

Base: Dict[str, Base] = declarative_base()
