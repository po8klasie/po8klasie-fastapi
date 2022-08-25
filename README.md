# po8klasie-api


## Local quick start

1. `docker-compose -f docker-compose.local.yml up --build`
2. Inside docker container `./cli.py regenerate_db`

## Env vars

- `DATABASE_URL`


## Commands

`./run.py <command>`

### `regenerate_db`

Bootstrap db. Run all jobs
