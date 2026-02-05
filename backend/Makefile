.PHONY: help init-db migrate upgrade downgrade run test clean

help:
	@echo "Available commands:"
	@echo "  make init-db      - Initialize database (create tables)"
	@echo "  make migrate      - Create new migration (usage: make migrate MESSAGE='description')"
	@echo "  make upgrade      - Apply all migrations"
	@echo "  make downgrade    - Rollback last migration"
	@echo "  make run          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean Python cache files"

init-db:
	alembic upgrade head

migrate:
	alembic revision --autogenerate -m "$(MESSAGE)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
