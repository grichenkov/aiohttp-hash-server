FROM python:3.11

WORKDIR /server

ENV POETRY_VERSION=1.8.3

RUN pip install poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY app ./app

ENV HOST=0.0.0.0
ENV PORT=8080

CMD poetry run aiohttp-hash-server --host $HOST --port $PORT
