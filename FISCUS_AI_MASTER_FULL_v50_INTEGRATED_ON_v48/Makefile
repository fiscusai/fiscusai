.PHONY: venv install run api dev db-up db-down lint fmt test migrate upgrade downgrade seed

VENV?=.venv
PY?=$(VENV)/bin/python
PIP?=$(VENV)/bin/pip
UVICORN?=$(VENV)/bin/uvicorn

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) apps.api.app.main:app --host 0.0.0.0 --port 8000 --reload

api: run

dev:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up --build

db-up:
	docker compose -f docker-compose.yml -f docker-compose.override.yml up -d db redis minio clamav

db-down:
	docker compose -f docker-compose.yml -f docker-compose.override.yml down

lint:
	$(PIP) install ruff
	ruff check apps/api/app

fmt:
	$(PIP) install ruff
	ruff format apps/api/app

test:
	$(PIP) install pytest
	$(VENV)/bin/pytest -q

migrate:
	alembic revision --autogenerate -m "auto"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

seed:
	$(PY) -c "from apps.api.app.db import init_db; init_db(); print('DB initialized');"
