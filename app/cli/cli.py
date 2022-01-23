import click as click

from app.cli.cli_logger import cli_logger


def get_data_source(data_provider_id: str, data_source_id: str):
    from app.data_providers.providers import data_providers

    try:
        return data_providers.get(data_provider_id)().sources.get(data_source_id)
    except KeyError:
        click.echo(
            f"{data_provider_id} provider with {data_source_id} source wasn't found",
            err=True,
        )


@click.group()
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict
    # (in case `cli()` is called without __name__ == "__main__")
    ctx.ensure_object(dict)


# --- Updating assets data


@cli.command("update_data_asset")
@click.argument("data_provider_id")
@click.argument("data_source_id")
def update_data_asset(data_provider_id, data_source_id):
    """Update asset file automatically"""
    get_data_source(data_provider_id, data_source_id).update_data_asset()


@cli.command("update_data_assets")
def update_data_assets():
    """Update assets files automatically"""
    from app.data_providers.providers import data_providers

    for data_provider in data_providers.values():
        cli_logger.info(f"Sourcing data from {data_provider.provider_id} provider")
        for source in data_provider().sources.values():
            try:
                source.update_data_asset()
                cli_logger.info(f"Updated data from {source.source_id} source")
            except Exception:
                cli_logger.info(
                    f"{source.source_id} doesn't allow automatic asset updates. Skipping."
                )


# --- Inserting assets data


@cli.command("insert_asset_data")
@click.argument("data_provider_id")
@click.argument("data_source_id")
def insert_asset_data(data_provider_id, data_source_id):
    """Inserts data from data asset to db"""
    get_data_source(data_provider_id, data_source_id).insert_data()


@cli.command("insert_assets_data")
def insert_assets_data():
    """Inserts data from data assets to db"""
    from app.data_providers.providers import data_providers

    for data_provider in data_providers.values():
        cli_logger.info(f"Inserting data from {data_provider.provider_id} provider")
        for source in data_provider().sources.values():
            cli_logger.info(f"Inserting data from {source.source_id} source")
            source.insert_data()
    cli_logger.info("Inserted assets data to db")


# --- Inserting projects


@cli.command("insert_projects")
def insert_projects():
    """Drops db data"""
    from app.projects.projects import insert_projects

    insert_projects()
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
    ctx.invoke(insert_projects)
    ctx.invoke(insert_assets_data)
