FROM python:3.11-buster as base


RUN apt-get update && apt-get install libpq5 -y

RUN pip install -U pip

FROM base as builder

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /server

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11-slim-buster as runtime

RUN apt-get update && apt-get install libpq5 -y
ENV VIRTUAL_ENV=/server/.venv \
    PATH="/server/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app ./app

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]