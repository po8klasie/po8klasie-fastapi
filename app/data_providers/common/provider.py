import os

from app.data_providers.common.file_utils import (
    save_data_asset,
    ensure_assets_dir,
    get_data_asset_filepath,
)


class DataProvider:
    provider_id: str
    source_configs = []
    _sources = {}

    @property
    def sources(self):
        if not self._sources:
            for SourceConfig in self.source_configs:
                source_config = SourceConfig(self)
                self._sources[source_config.source_id] = source_config
        return self._sources


class DataSource:
    source_id: str
    asset_ext: str
    provider: DataProvider

    def __init__(self, provider):
        if not provider:
            raise Exception("DataSource class was called without provider argument")
        self.provider = provider

        ensure_assets_dir(self.provider.provider_id)

    def save_data_asset(self, data):
        try:
            filepath = self.get_data_asset_filepath()
            os.remove(filepath)
        except Exception:
            pass
        save_data_asset(
            data=data,
            data_provider_id=self.provider.provider_id,
            data_source_id=self.source_id,
            ext=self.asset_ext,
        )

    def get_data_asset_filepath(self):
        filepath = get_data_asset_filepath(
            data_provider_id=self.provider.provider_id,
            data_source_id=self.source_id,
            ext=self.asset_ext,
        )
        if not filepath:
            raise Exception(f"Could't find {self.source_id} source assets files")
        return filepath

    def update_asset(self):
        raise Exception(
            f"{self.source_id} source does not allow getting new data assets automatically"
        )
