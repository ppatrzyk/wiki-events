{{ config(order_by='(event_type, bot)', engine='MergeTree()', materialized='table') }}

select
    event_type,
    bot,
    count(*) as events
from {{ ref('wiki') }}
group by event_type, bot
