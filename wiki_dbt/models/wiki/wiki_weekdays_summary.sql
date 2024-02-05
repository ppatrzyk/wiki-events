{{ config(order_by='(wiki_name, weekday, hour)', engine='MergeTree()', materialized='table') }}

select
    wiki_name,
    dateName('weekday', interval) as weekday,
    dateName('hour', interval) as hour,
    avg(events) as events
from {{ ref('wiki_hourly_bywiki_summary') }}
group by wiki_name, weekday, hour
