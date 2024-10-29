SELECT
    *,
    CURRENT_DATE::DATE AS record_created_dt
FROM
    recsys.games_description