{{ config(materialized='incremental', unique_key='order_id') }}
select
  o.order_id,
  o.customer_id,
  o.order_ts,
  o.currency,
  o.total_amount_eur,
  o.updated_at
from {{ ref('stg_orders') }} o
{% if is_incremental() %}
where o.updated_at > (select coalesce(max(updated_at), timestamp '1900-01-01') from {{ this }})
{% endif %}
