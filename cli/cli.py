import click as click

from cli.cli_logger import cli_logger


@click.group()
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict
    # (in case `cli()` is called without __name__ == "__main__")
    ctx.ensure_object(dict)


# --- Jobs


@cli.command("create_institution_records")
def create_institution_records_command():
    """Create institution records"""
    from jobs.create_institution_records import create_institution_records

    create_institution_records()

    cli_logger.info("Created institution records")


@cli.command("add_gdynia_api_data_to_records")
def add_gdynia_api_data_to_records_command():
    """Add Gdynia API data to records"""
    from jobs.add_gdynia_api_data_to_records import add_gdynia_api_data_to_records

    add_gdynia_api_data_to_records()

    cli_logger.info("Added Gdynia API data to records")


@cli.command("apply_data_patches")
def apply_data_patches_command():
    """Apply data patches to institutions records"""
    from jobs.apply_data_patches import apply_data_patches

    apply_data_patches()

    cli_logger.info("Applied data patches to institutions records")


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
    from db.db_regeneration_utils import create_all

    create_all()
    cli_logger.info("Created db schema")


@cli.command("drop_db")
def drop_db():
    """Drop db data"""
    from db.db_regeneration_utils import drop_all

    drop_all()
    cli_logger.info("Dropped db")


@cli.command("regenerate_db")
@click.pass_context
def regenerate_db_command(ctx):
    """Regenerate db"""
    ctx.invoke(drop_db)
    ctx.invoke(create_db_schema)
    ctx.invoke(create_project_records_command)
    ctx.invoke(create_institution_records_command)
    ctx.invoke(add_gdynia_api_data_to_records_command)
    ctx.invoke(apply_data_patches_command)
