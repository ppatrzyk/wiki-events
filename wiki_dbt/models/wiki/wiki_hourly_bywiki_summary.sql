{{ config(order_by='(interval, wiki_name)', engine='MergeTree()', materialized='incremental', unique_key='(interval, wiki_name)', incremental_strategy='append') }}

select 
    toStartOfHour(created_at) as interval,
    wiki_name,
    count(*) as events,
    now() as update_time
from {{ ref('wiki') }}
group by toStartOfHour(created_at), wiki_name
having 
    interval < toStartOfHour(now())
    {% if is_incremental() %}
    and interval > (select max(interval) from {{this}})
    {% endif %}
