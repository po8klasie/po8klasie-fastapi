import yaml
import glob

from run.cli_logger import cli_logger
from db.db import get_db
from app.project.models import Project

config_files = glob.glob("./app/project/configs/*.yml")


def parse_config_file(filename):
    with open(filename, "r") as stream:
        try:
            parsed = yaml.safe_load(stream)
            return parsed
        except yaml.YAMLError as exc:
            cli_logger.error(exc)


def create_project_records():
    db = next(get_db())
    for config_file in config_files:
        project_config = parse_config_file(config_file)
        db.add(Project(**project_config))
    db.commit()
    cli_logger.info("Added project")
