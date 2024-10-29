SELECT
    *,
    CURRENT_DATE::DATE AS record_created_dt
FROM
    {{ SCHEMA_NAME }}.{{ TABLE_NAME }}