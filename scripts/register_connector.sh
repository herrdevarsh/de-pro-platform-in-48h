#!/usr/bin/env bash
set -euo pipefail
echo "Registering Debezium Postgres connector..."
curl -sS -X PUT http://localhost:8083/connectors/postgres-cdc/config \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "connector.class":"io.debezium.connector.postgresql.PostgresConnector",
  "database.hostname":"postgres",
  "database.port":"5432",
  "database.user":"demo",
  "database.password":"demo",
  "database.dbname":"ecommerce",
  "topic.prefix":"ecom",
  "slot.name":"debezium",
  "publication.autocreate.mode":"filtered",
  "schema.include.list":"public",
  "table.include.list":"public.customers,public.orders,public.events",
  "tombstones.on.delete":"false",
  "plugin.name":"pgoutput",
  "decimal.handling.mode":"double",
  "time.precision.mode":"adaptive_time_microseconds"
}
JSON
echo "Connector registered."
