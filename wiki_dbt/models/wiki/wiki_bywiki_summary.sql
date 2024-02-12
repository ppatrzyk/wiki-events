{{ config(order_by='wiki_name', engine='MergeTree()', materialized='table') }}

select
    wiki_name,
    sum(events) as events
from {{ ref('wiki_hourly_bywiki_summary') }}
group by wiki_name
