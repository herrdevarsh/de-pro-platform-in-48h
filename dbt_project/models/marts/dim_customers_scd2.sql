{{ config(materialized='table') }}
select
  customer_id,
  email,
  country,
  created_at,
  is_active
from {{ ref('stg_customers') }}
