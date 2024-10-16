{{ config(materialized='table') }}


{% import dbt_utils %}


with filtered_data AS (
    SELECT * 
    FROM {{source('public', 'detected_images')}}
)

SELECT
    {{ dbt_utils.unique_id() }} as ID,
    *
FROM filtered_data