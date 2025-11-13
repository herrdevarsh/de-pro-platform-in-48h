.PHONY: setup up down dbt stream demo connector demo-docker-psql

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down -v

dbt:
	cd dbt_project && dbt deps && dbt snapshot --profiles-dir . && dbt run --profiles-dir . && dbt test --profiles-dir .

stream:
	BROKER=localhost:9092 LAKE_DIR=./lake . .venv/bin/activate; python stream/processor.py

demo:
	./scripts/psql_demo.sh

demo-docker-psql:
	./scripts/psql_demo_docker.sh

connector:
	./scripts/register_connector.sh
