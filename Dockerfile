
FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --upgrade pip
RUN pip install uv
RUN uv sync --locked --no-dev

COPY . .

ENV PYTHONUNBUFFERED=1
