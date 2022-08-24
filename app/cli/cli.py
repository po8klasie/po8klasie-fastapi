import click as click

from app.cli.cli_logger import cli_logger
from app.jobs.add_gdynia_api_data_to_records import add_gdynia_api_data_to_records
from app.jobs.create_facility_records import create_facility_records


@click.group()
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict
    # (in case `cli()` is called without __name__ == "__main__")
    ctx.ensure_object(dict)


# --- Jobs


@cli.command("create_facility_records")
def create_facility_records_command():
    create_facility_records()


@cli.command("add_gdynia_api_data_to_records")
def add_gdynia_api_data_to_records_command():
    add_gdynia_api_data_to_records()


# --- Inserting projects


@cli.command("create_project_records")
def create_project_records_command():
    from app.projects.add_project_records import create_project_records

    create_project_records()

    cli_logger.info("inserted projects to db")


# --- DB utils


@cli.command("create_db_schema")
def create_db_schema():
    """Create db schema"""
    from app.db.db_utils import create_all

    create_all()
    cli_logger.info("Created db schema")


@cli.command("drop_db")
def drop_db():
    """Drops db data"""
    from app.db.db_utils import drop_all

    drop_all()
    cli_logger.info("Dropped db")


@cli.command("prepare_db")
@click.pass_context
def prepare_db(ctx):
    """Prepare db"""
    ctx.invoke(drop_db)
    ctx.invoke(create_db_schema)
    ctx.invoke(create_project_records_command)
    ctx.invoke(create_facility_records_command)
    ctx.invoke(add_gdynia_api_data_to_records_command)
