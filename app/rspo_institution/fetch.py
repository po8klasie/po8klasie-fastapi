import itertools
from typing import Dict

from requests import Session
import json
from cli.cli_logger import cli_logger


BASE_URL = "http://api-rspo.mein.gov.pl"


def create_rspo_r_session():
    s = Session()
    s.headers = {"Accept": "application/ld+json"}
    s.verify = False
    return s


# 93 => "Branżowa szkoła I stopnia"
# 94 => "Branżowa szkoła II stopnia"
# 14 => "Liceum ogólnokształcące"
# 15 => "Liceum profilowane"
# 27 => "Liceum sztuk plastycznych"
# 20 => "Szkoła specjalna przysposabiająca do pracy"
# 16 => "Technikum"
RELEVANT_FACILITY_TYPE_IDS = [93, 94, 14, 15, 27, 16]


def fetch(path: str, r_session: Session, params: Dict[str, str] = None):
    res = r_session.get(
        BASE_URL + path,
        params=params,
    )
    cli_logger.info(f"Fetching {res.url}")
    return res.json()


def fetch_institution_data(
    r_session: Session, params: Dict[str, str] = None, page_limit: int = None
):
    counter = 0
    next_api_page_url = "/api/placowki/?page=1"  # doesn't work w/o page=1
    has_reached_end = False
    i = 0

    cli_logger.info(
        f"Starting fetching RSPO API data for params \n {json.dumps(params, indent = 4)}"
    )

    while not has_reached_end:
        if page_limit and i + 1 > page_limit:
            cli_logger.info(f"Page limit ({page_limit}) has been reached. Aborting.")
            break
        if not next_api_page_url:
            raise Exception("Next api page is not defined")

        api_page_data = fetch(next_api_page_url, r_session, params)
        items = api_page_data.get("hydra:member", [])

        counter += len(items)

        for item in items:
            yield item

        cli_logger.info(
            f"Fetched RSPO API page {i}. "
            f"Collected {counter}/{api_page_data.get('hydra:totalItems')} items"
        )

        next_api_page_url = api_page_data.get("hydra:view", {}).get("hydra:next")
        if not next_api_page_url:
            has_reached_end = True

        i += 1

        cli_logger.info("Fetched RSPO API data")


def fetch_borough_rspo_institution_data(borough_name: str):
    params_list = [
        {"powiat_nazwa": borough_name, "typ_podmiotu_id": institution_type_id}
        for institution_type_id in RELEVANT_FACILITY_TYPE_IDS
    ]

    with create_rspo_r_session() as r_session:
        return itertools.chain.from_iterable(
            [fetch_institution_data(r_session, params) for params in params_list]
        )
