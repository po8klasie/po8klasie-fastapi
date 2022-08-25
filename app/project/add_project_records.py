import glob

from cli.cli_logger import cli_logger

from app.lib.yaml_utils import parse_yaml_file
from db.db import get_db
from app.project.models import Project

config_files = glob.glob("./app/project/configs/*.yml")


def create_project_records():
    db = next(get_db())
    for config_file in config_files:
        project_config = parse_yaml_file(config_file)
        db.add(Project(**project_config))
    db.commit()
    cli_logger.info("Added project")
