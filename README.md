# po8klasie-fastapi


## Local quick start

Run the app `docker-compose -f docker-compose.local.yml up --build`


## Data management

You can populate db using [po8klasie-data-management-example repo](https://github.com/po8klasie/po8klasie-data-management-example) 

More info about:
* how we add data to the db
* how you can integrate your own data with po8klasie backend

is available in [po8klasie-data-sources repo](https://github.com/po8klasie/po8klasie-data-sources) 


## Env vars

* `DATABASE_URL` required
* `TEST_DATABASE_URL` database for tests (optional)
* `SENTRY_DSN` (optional)
* `ENVIRONMENT` (optional)