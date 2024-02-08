{{ config(order_by='wiki_name', engine='MergeTree()', materialized='table') }}

select
    wiki_name,
    count(*) as events
from {{ ref('wiki') }}
group by wiki_name
