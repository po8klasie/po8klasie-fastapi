# po8klasie-api


## Local quick start

1. `docker-compose -f docker-compose.local.yml up --build`
2. Inside docker container `./run.py regenerate_db`

## Env vars

- `DATABASE_URL`


## Commands

`./run.py <command>`

### `regenerate_db`

Bootstrap db. Run all jobs


## Data patches
In some cases we want to overwrite institutions data which has been fetched from the APIs.
To do so, please edit `app/institution/data_patches/patches.yml`
