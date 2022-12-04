#!/bin/bash

if [[ "${DATABASE_CERT}" ]]; then
  echo "DB_CERT env var detected. Dumping certificate to db_cert.crt file"
  printf %b "$DATABASE_CERT" > "db_cert.crt"
fi


while ! </dev/tcp/db/5432; do
  sleep 1
done

uvicorn app.main:app --host 0.0.0.0 --reload
