from typing import Dict

import requests

from app.cli.cli_logger import cli_logger

BASE_URL = "http://194.54.26.132"


def fetch(path: str, params: Dict[str, str] = None):
    res = requests.get(
        BASE_URL + path, headers={"Accept": "application/ld+json"}, params=params
    )
    cli_logger.info(f"Fetching {res.url}")
    return res.json()


def fetch_rspo_api_data(params: Dict[str, str] = None, page_limit: int = None):
    api_data = []
    next_api_page_url = "/api/placowki/"
    has_reached_end = False
    i = 0

    while not has_reached_end:
        if page_limit and i + 1 > page_limit:
            cli_logger.info(f"Page limit ({page_limit}) has been reached. Aborting.")
            break
        if not next_api_page_url:
            raise Exception("Next api page is not defined")

        api_page_data = fetch(next_api_page_url, params)
        api_data += api_page_data.get("hydra:member", [])

        cli_logger.info(
            f"Fetched RSPO API page {i}. "
            f"Collected {len(api_data)}/{api_page_data.get('hydra:totalItems')} items"
        )

        next_api_page_url = api_page_data.get("hydra:view", {}).get("hydra:next")
        if not next_api_page_url:
            has_reached_end = True

        i += 1

        cli_logger.info("Fetched RSPO API data")

    return api_data
