FROM python:3.12-slim as base

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

COPY . .

FROM base as production

RUN poetry install --no-interaction --no-ansi --only main

CMD ["uvicorn", "back.main:app", "--host", "0.0.0.0", "--port", "8000"]