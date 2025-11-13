{{ config(materialized='view') }}
select
  customer_id::bigint as customer_id,
  email,
  country,
  cast(created_at as timestamp) as created_at,
  cast(updated_at as timestamp) as updated_at,
  is_active::boolean as is_active
from read_parquet('lake/raw/customers/*/*.parquet')
