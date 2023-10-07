FROM python:3.11 AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8

ARG PY_SHORT_VERSION=3.11

FROM base AS builder
RUN apt-get update
RUN apt-get install -y gcc gdal-bin g++ libgdal-dev python3-gdal
RUN pip install --upgrade pip

COPY Pipfile.lock ./
COPY Pipfile ./

RUN pip install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd --no-create-home appuser

WORKDIR /app
USER appuser
ENV PYTHONPATH="/app"
