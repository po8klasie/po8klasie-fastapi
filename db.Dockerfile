FROM postgres:14


RUN apt-get update && apt-get install -y postgresql-14-postgis-3

COPY ./db/init.sql /docker-entrypoint-initdb.d/db.sql

CMD ["/usr/local/bin/docker-entrypoint.sh","postgres"]