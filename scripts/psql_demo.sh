#!/usr/bin/env bash
set -euo pipefail
psql postgres://demo:demo@localhost:5432/ecommerce -c "insert into orders(order_id,customer_id,order_ts,currency,total_amount_eur,updated_at) values (floor(extract(epoch from now())),1,now(),'EUR',round(random()*100+20,2),now());"
echo "Inserted demo order."
