import click as click

from cli.cli_logger import cli_logger


@click.group()
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict
    # (in case `cli()` is called without __name__ == "__main__")
    ctx.ensure_object(dict)


# --- Jobs


@cli.command("create_facility_records")
def create_facility_records_command():
    """Create facility records"""
    from jobs.create_facility_records import create_facility_records

    create_facility_records()

    cli_logger.info("Created facility records")


@cli.command("add_gdynia_api_data_to_records")
def add_gdynia_api_data_to_records_command():
    """Add Gdynia API data to records"""
    from jobs.add_gdynia_api_data_to_records import add_gdynia_api_data_to_records

    add_gdynia_api_data_to_records()

    cli_logger.info("Added Gdynia API data to records")


# --- Projects


@cli.command("create_project_records")
def create_project_records_command():
    """Create project records"""
    from app.project.add_project_records import create_project_records

    create_project_records()

    cli_logger.info("Created project records")


# --- DB utils


@cli.command("create_db_schema")
def create_db_schema():
    """Create db schema"""
    from db.db_utils import create_all

    create_all()
    cli_logger.info("Created db schema")


@cli.command("drop_db")
def drop_db():
    """Drop db data"""
    from db.db_utils import drop_all

    drop_all()
    cli_logger.info("Dropped db")


@cli.command("regenerate_db")
@click.pass_context
def regenerate_db_command(ctx):
    """Regenerate db"""
    ctx.invoke(drop_db)
    ctx.invoke(create_db_schema)
    ctx.invoke(create_project_records_command)
    ctx.invoke(create_facility_records_command)
    ctx.invoke(add_gdynia_api_data_to_records_command)
