FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini .
COPY ./scripts ./scripts

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
