{% macro primary_key(columns) %}
  {{ adapter.dispatch('primary_key','ETH_MedData_Warehouse') (columns) }}
{% endmacro %}

{% macro default__primary_key(columns) %}
  ALTER TABLE {{ this }} ADD PRIMARY KEY ({{ columns | join(', ') }});
{% endmacro %}