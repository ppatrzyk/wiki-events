{{ config(order_by='(wiki_name, weekday, hour)', engine='MergeTree()', materialized='table') }}

select
    wiki_name,
    cast(toDayOfWeek(interval, 0), 'String') || '_' || dateName('weekday', interval) as weekday,
    toHour(interval) as hour,
    avg(events) as events
from {{ ref('wiki_hourly_bywiki_summary') }}
group by wiki_name, weekday, hour
