{{ config(materialized='view') }}
select
  order_id::bigint as order_id,
  customer_id::bigint as customer_id,
  cast(order_ts as timestamp) as order_ts,
  currency,
  cast(total_amount_eur as double) as total_amount_eur,
  cast(updated_at as timestamp) as updated_at
from read_parquet('lake/raw/orders/*/*.parquet')
