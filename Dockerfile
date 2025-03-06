# Базовый образ Python с поддержкой Poetry
FROM python:3.12-slim as base

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Копируем зависимости
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

# Копируем исходный код
COPY . .

# Этап для production
FROM base as production

# Устанавливаем только runtime зависимости
RUN poetry install --no-interaction --no-ansi --only main

# Команда запуска (будет переопределена в docker-compose для разных сервисов)
CMD ["uvicorn", "back.main:app", "--host", "0.0.0.0", "--port", "8000"]