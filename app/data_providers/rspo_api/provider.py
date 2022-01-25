import json

from app.data_providers.common.provider import DataProvider, DataSource
from app.data_providers.rspo_api.fetch_utils import fetch_rspo_api_data


def create_models_from_file(filepath, project_id):
    from app.data_providers.rspo_api.parser import create_model_from_facility_data
    from app.db.db import get_db

    db = next(get_db())
    with open(filepath) as f:
        facilities_data = json.load(f)
        for facility_data in facilities_data:
            db.add(
                create_model_from_facility_data(
                    db, facility_data, project_id=project_id
                )
            )
        db.commit()


entity_codes_and_ids = {
    "Liceum ogólnokształcące": (14, "licea_ogolnoksztalcace"),
    "Liceum profilowane": (15, "licea_profilowane"),
    "Liceum ogólnokształcące uzupełniające dla absolwentów zasadniczych szkół zawodowych": (
        17,
        "licea_uzupelniajace",
    ),
    "Technikum": (16, "technika"),
    "Branżowa szkoła I stopnia": (93, "branzowe_I_stopnia"),
    "Branżowa szkoła II stopnia": (94, "branzowe_II_stopnia"),
    "Bednarska Szkoła Realna": (90, "bednarska"),
}


class RspoApiAbstractSourceConfig(DataSource):
    asset_ext = "json"
    source_id: str
    project_id: str
    params = {}

    def update_data_asset(self):
        self.save_data_asset(json.dumps(fetch_rspo_api_data(params=self.params)))

    def insert_data(self):
        print(self.source_id, self.get_data_asset_filepath())
        create_models_from_file(
            self.get_data_asset_filepath(), project_id=self.project_id
        )


def warszawa_source_configs_factory():
    source_configs = []
    for entity_code, entity_name in entity_codes_and_ids.values():

        class WarsawSourceConfig(RspoApiAbstractSourceConfig):
            source_id = f"warszawa_{entity_name}"
            project_id = "warszawa"
            params = {"powiat_nazwa": "Warszawa", "typ_podmiotu_id": entity_code}

        source_configs.append(WarsawSourceConfig)
    return source_configs


def gdynia_source_configs_factory():
    source_configs = []
    for entity_code, entity_name in entity_codes_and_ids.values():

        class GdyniaSourceConfig(RspoApiAbstractSourceConfig):
            source_id = f"gdynia_{entity_name}"
            project_id = "gdynia"
            params = {"powiat_nazwa": "Gdynia", "typ_podmiotu_id": entity_code}

        source_configs.append(GdyniaSourceConfig)
    return source_configs


class RspoApiDataProviderConfig(DataProvider):
    provider_id = "rspo_api"
    source_configs = [
        *warszawa_source_configs_factory(),
        *gdynia_source_configs_factory(),
    ]
