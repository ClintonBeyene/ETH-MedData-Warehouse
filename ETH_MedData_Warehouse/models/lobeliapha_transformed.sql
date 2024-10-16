{{config(materialized='table')}}

with filtered_data AS (
    SELECT * 
    FROM {{source('public', 'lobeliacosmetics')}}
)

SELECT
    "ID", 
    Date,
    Product_Name,
    Weight,
    Price,
    "Telegram Address",
    Address,
    "Phone Number",
    "Delivery Fee",
    "Media Path"
FROM filtered_data