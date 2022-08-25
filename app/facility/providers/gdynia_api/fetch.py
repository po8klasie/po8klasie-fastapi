import requests

from cli.cli_logger import cli_logger


BASE_URL = "https://edukacja.gdynia.pl/api"


def fetch_gdynia_facility_data():
    res = requests.get(BASE_URL + "/schools")
    cli_logger.info(f"Fetching {res.url}")
    return res.json()
