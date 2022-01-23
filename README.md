# po8klasie-api


## Local quick start

1. `docker-compose -f docker-compose.local.yml up --build`
2. Inside docker container `./cli.py prepare_db`

To update providers data run `./cli.py update_data_assets`

DO NOT DELETE EMPTY JSON FILES from data_assets dir.

API swagger is hosted at /docs
