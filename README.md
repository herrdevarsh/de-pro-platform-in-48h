# de-pro-platform-in-48h

End-to-end **CDC → streaming → lake → warehouse** mini data platform.

**Stack**
- Postgres (OLTP) → Debezium (CDC) → Redpanda (Kafka-compatible)
- Python stream processor → Parquet lake (partitioned by ingest_date)
- dbt + DuckDB warehouse (incremental models, SCD2 snapshot)
- Airflow DAG for orchestration
- dbt tests for data quality

## Quickstart
```bash
make up
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
make connector                  # register Debezium CDC connector
make stream                     # run the lake writer (or: python stream/processor.py)
make demo                       # insert a new order via psql
make dbt                        # snapshot/run/test models
```
If you don't have `psql` installed: `make demo-docker-psql`.

Airflow UI: http://localhost:8080 (admin/admin)  
Redpanda Console: http://localhost:8081

## What this proves
- Real-time CDC ingestion (Debezium) into a durable log (Redpanda).
- Streaming land to Parquet with date partitions.
- Incremental warehouse model by `updated_at`, plus SCD2 snapshot.
- Orchestrated daily with Airflow; tested with dbt.

Small doc tweak to create PR diff.
