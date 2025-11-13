{{ config(materialized='table') }}
with base as (
  select
    session_id,
    min(event_ts) as session_start,
    max(event_ts) as session_end,
    count(*) filter (where event_type='purchase') as purchases
  from {{ ref('stg_events') }}
  group by 1
)
select * from base
