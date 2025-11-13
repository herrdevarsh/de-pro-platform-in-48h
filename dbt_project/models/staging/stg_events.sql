{{ config(materialized='view') }}
select
  event_id::bigint as event_id,
  customer_id::bigint as customer_id,
  cast(event_ts as timestamp) as event_ts,
  event_type,
  session_id,
  cast(updated_at as timestamp) as updated_at
from read_parquet('lake/raw/events/*/*.parquet')
