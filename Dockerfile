
FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project

COPY . .

FROM python:3.13-slim AS production

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /app /app

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "back.main:app", "--host", "0.0.0.0", "--port", "8000"]
