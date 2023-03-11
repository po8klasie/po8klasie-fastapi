import yaml

from cli.cli_logger import cli_logger


def parse_yaml_file(filename):
    with open(filename, "r") as stream:
        try:
            parsed = yaml.safe_load(stream)
            return parsed
        except yaml.YAMLError as exc:
            cli_logger.error(exc)
