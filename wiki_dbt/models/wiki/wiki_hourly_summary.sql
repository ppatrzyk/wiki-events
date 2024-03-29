{{ config(order_by='interval', engine='MergeTree()', materialized='incremental', unique_key='interval', incremental_strategy='append') }}

select 
    toStartOfHour(created_at) as interval,
    count(*) as events,
    now() as update_time
from {{ ref('wiki') }}
group by toStartOfHour(created_at)
having 
    interval < toStartOfHour(now())
    {% if is_incremental() %}
    and interval > (select max(interval) from {{this}})
    {% endif %}
