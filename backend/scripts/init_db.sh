#!/bin/bash
# Скрипт для инициализации базы данных

echo "Applying database migrations..."
alembic upgrade head

echo "Database initialized successfully!"
