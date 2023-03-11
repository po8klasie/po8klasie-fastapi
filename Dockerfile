FROM python:3.10-slim

RUN mkdir -p /opt/po8klasie-fastapi

WORKDIR /opt/po8klasie-fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/opt/po8klasie-fastapi"
ENV POETRY_VERSION 1.4.0
ENV POETRY_VIRTUALENVS_CREATE false

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-ansi

COPY . .

ENTRYPOINT ./entrypoint.sh