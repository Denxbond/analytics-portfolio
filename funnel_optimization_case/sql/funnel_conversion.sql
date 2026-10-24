-- Funnel conversion metrics by marketing channel
-- Assumes one raw event row per event with a stable user ID and UTC event time.
-- Conversion is a first deposit in [registration, registration + 7 days).
WITH registrations AS (
    SELECT
        user_id,
        event_timestamp AS registration_timestamp,
        marketing_channel,
        country,
        device,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_timestamp) AS registration_rank
    FROM raw_player_events
    WHERE event_type = 'registration'
),
eligible_registrations AS (
    SELECT * FROM registrations WHERE registration_rank = 1
),
first_deposits AS (
    SELECT
        r.user_id,
        MIN(d.event_timestamp) AS first_deposit_timestamp
    FROM eligible_registrations r
    LEFT JOIN raw_player_events d
      ON d.user_id = r.user_id
     AND d.event_type = 'deposit'
     AND d.event_timestamp >= r.registration_timestamp
     AND d.event_timestamp < r.registration_timestamp + INTERVAL '7 days'
    GROUP BY r.user_id
),
joined AS (
    SELECT
        r.user_id,
        r.registration_timestamp,
        r.marketing_channel,
        r.country,
        r.device,
        d.first_deposit_timestamp,
        CASE WHEN d.first_deposit_timestamp IS NOT NULL THEN 1 ELSE 0 END AS converted_7d
    FROM eligible_registrations r
    LEFT JOIN first_deposits d ON r.user_id = d.user_id
)
SELECT
    marketing_channel,
    COUNT(DISTINCT user_id) AS registrations,
    SUM(converted_7d) AS first_time_depositors_7d,
    ROUND(SUM(converted_7d)::NUMERIC / NULLIF(COUNT(DISTINCT user_id), 0), 4) AS reg_to_dep_conversion_rate_7d
FROM joined
GROUP BY 1
ORDER BY reg_to_dep_conversion_rate_7d DESC;
