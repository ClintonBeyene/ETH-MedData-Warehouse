
  
    

  create  table "ETH-MedData-Warehouse"."public"."lobeliapha_transformed__dbt_tmp"
  
  
    as
  
  (
    

with filtered_data AS (
    SELECT * 
    FROM "ETH-MedData-Warehouse"."public"."lobeliacosmetics"
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
    "Delivery Fee"
FROM filtered_data
  );
  