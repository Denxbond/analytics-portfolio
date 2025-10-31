-- Aggregate most common navigation paths and their conversion performance.
WITH ordered_events AS (
    SELECT
        user_id,
        event_type,
        event_index,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_index) AS step_position
    FROM user_clickstream
),
user_paths AS (
    SELECT
        user_id,
        STRING_AGG(event_type, ' > ' ORDER BY step_position) AS path,
        MAX(CASE WHEN event_type = 'deposit' THEN 1 ELSE 0 END) AS converted
    FROM ordered_events
    WHERE step_position <= 5
    GROUP BY user_id
)
SELECT
    path,
    COUNT(*) AS users,
    SUM(converted) AS deposits,
    ROUND(SUM(converted)::NUMERIC / NULLIF(COUNT(*), 0), 4) AS conversion_rate
FROM user_paths
GROUP BY path
ORDER BY users DESC, conversion_rate DESC
LIMIT 20;
