FROM python:3.10-slim

RUN mkdir -p /opt/opendata-api

WORKDIR /opt/po8klasie-fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/opt/po8klasie-fastapi"


COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

ENTRYPOINT entrypoint.sh