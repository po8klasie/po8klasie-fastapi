import os
import re
from datetime import datetime
from pathlib import Path

from app.config import settings

DATE_STRING_FORMAT = "%Y-%m-%d_%H:%M:%S"
DATE_STRING_REGEX = r"^.+_(\d+-\d+-\d+_\d+:\d+:\d+)\..*$"


def save_data_asset(data, data_provider_id, data_source_id, ext):
    date_string = datetime.now().strftime(DATE_STRING_FORMAT)
    filename = f"{data_source_id}_{date_string}.{ext}"
    filepath = os.path.join(settings.data_assets_root_dir, data_provider_id, filename)
    with open(filepath, "w") as f:
        f.write(data)


def get_data_asset_filepath(data_provider_id: str, data_source_id: str, ext: str):
    assets_dir = os.path.join(settings.data_assets_root_dir, data_provider_id)
    for root, dirs, files in os.walk(assets_dir):
        for filename in files:
            date_string = re.search(DATE_STRING_REGEX, filename)
            if date_string and filename == f"{data_source_id}_{date_string.group(1)}.{ext}":
                return os.path.join(assets_dir, filename)


def ensure_assets_dir(data_provider_id):
    dir_path = os.path.join(settings.data_assets_root_dir, data_provider_id)
    Path(dir_path).mkdir(parents=True, exist_ok=True)
