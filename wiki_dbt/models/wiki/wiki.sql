{{ config(order_by='created_at', engine='MergeTree()', materialized='incremental', unique_key='id', incremental_strategy='append') }}

select 
    id,
    created_at,
    JSON_VALUE(data_raw_json, '$.meta.dt') as event_time,
    JSON_VALUE(data_raw_json, '$.type') as event_type,
    JSON_VALUE(data_raw_json, '$.meta.domain') as domain,
    JSON_VALUE(data_raw_json, '$.wiki') as wiki_name,
    JSON_VALUE(data_raw_json, '$.bot') as bot
from wiki_raw
{% if is_incremental() %}
where created_at > (select max(created_at) from {{this}})
{% endif %}
