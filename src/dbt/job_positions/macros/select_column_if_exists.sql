{#
    This macro selects a column if exists in the table 
#}

{% macro select_column_if_exists(table, column) %}
  {% set columns = adapter.get_columns_in_relation(table) %}
  {% if column in columns | map(attribute='name') %}
    {{ column }}
  {% else %}
    NULL as {{ column }}
  {% endif %}
{% endmacro %}