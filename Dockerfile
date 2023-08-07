FROM python:3.11.0-alpine AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN apk add build-base libffi-dev
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi --no-root

FROM python:3.11.0-alpine

RUN apk add ffmpeg

WORKDIR /app

COPY --from=builder /app /app
ADD . /app

CMD /app/.venv/bin/python main.py