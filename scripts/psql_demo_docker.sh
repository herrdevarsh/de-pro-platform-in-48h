#!/usr/bin/env bash
set -euo pipefail
CID=$(docker ps --format '{{.Names}}' | grep -E 'postgres|ecommerce' || true)
if [ -z "$CID" ]; then
  CID=$(docker ps --format '{{.Names}}' | grep 'de-pro-platform-in-48h-postgres-1' || true)
fi
if [ -z "$CID" ]; then
  echo "Couldn't find the Postgres container. Is 'docker compose up' running?"; exit 1;
fi
docker exec -it "$CID" psql -U demo -d ecommerce -c "insert into orders(order_id,customer_id,order_ts,currency,total_amount_eur,updated_at) values (floor(extract(epoch from now())),1,now(),'EUR',round(random()*100+20,2),now());"
echo "Inserted demo order via Docker psql."
