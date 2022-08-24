# po8klasie-api


## Local quick start

1. `docker-compose -f docker-compose.local.yml up --build`
2. Inside docker container `./cli.py prepare_db`

## Env vars

- `DATABASE_URL`


## Commands

`./cli.py <command>`

### `prepare_db`

Bootstrap db. Run all jobs
