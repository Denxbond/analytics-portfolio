-- Funnel conversion metrics by marketing channel
WITH registrations AS (
    SELECT
        user_id,
        registration_date,
        marketing_channel,
        country,
        device
    FROM raw_player_events
    WHERE event_type = 'registration'
),
deposits AS (
    SELECT
        user_id,
        MIN(event_timestamp) AS first_deposit_date,
        SUM(deposit_amount) AS total_deposit_amount
    FROM raw_player_events
    WHERE event_type = 'deposit'
    GROUP BY 1
),
joined AS (
    SELECT
        r.user_id,
        r.registration_date,
        r.marketing_channel,
        r.country,
        r.device,
        d.first_deposit_date,
        d.total_deposit_amount,
        CASE WHEN d.user_id IS NOT NULL THEN 1 ELSE 0 END AS converted
    FROM registrations r
    LEFT JOIN deposits d ON r.user_id = d.user_id
)
SELECT
    marketing_channel,
    COUNT(*) AS registrations,
    SUM(converted) AS first_time_depositors,
    ROUND(SUM(converted)::NUMERIC / NULLIF(COUNT(*), 0), 4) AS reg_to_dep_conversion_rate,
    ROUND(SUM(total_deposit_amount)::NUMERIC / NULLIF(COUNT(*), 0), 2) AS arpu,
    ROUND(SUM(total_deposit_amount)::NUMERIC / NULLIF(NULLIF(SUM(converted),0),0), 2) AS arppu
FROM joined
GROUP BY 1
ORDER BY reg_to_dep_conversion_rate DESC;
