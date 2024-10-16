{{ config(materialized='table') }}

{% import dbt_utils %}

with filtered_data AS (
    SELECT * 
    FROM {{source('public', 'Telegram')}}
)

SELECT
    {{ dbt_utils.surrogate_key() }} as ID,
    *
FROM filtered_data