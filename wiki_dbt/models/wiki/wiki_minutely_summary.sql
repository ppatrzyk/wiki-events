{{ config(order_by='interval', engine='MergeTree()', materialized='incremental', unique_key='interval', incremental_strategy='append') }}

select 
    toStartOfMinute(time) as interval,
    count(*) as events,
    now() as update_time
from wiki
group by toStartOfMinute(time)
having 
    interval < toStartOfMinute(now())
    {% if is_incremental() %}
    and interval > (select max(interval) from {{this}})
    {% endif %}
