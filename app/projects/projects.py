from app.db.db import get_db
from app.projects.configs.gdynia import gdynia_project_config
from app.projects.configs.warszawa import warszawa_project_config

projects = {
    warszawa_project_config.project_id: warszawa_project_config,
    gdynia_project_config.project_id: gdynia_project_config,
}


def insert_projects():
    db = next(get_db())
    for project_config in projects.values():
        db.add(project_config)
    db.commit()
