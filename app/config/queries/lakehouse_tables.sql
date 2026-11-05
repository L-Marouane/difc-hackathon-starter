-- Tables built so far in the medallion layers. Fills up as the founder builds the pipeline.
SELECT
  table_schema AS layer,
  table_name,
  CASE table_type
    WHEN 'STREAMING_TABLE' THEN 'streaming table'
    WHEN 'MATERIALIZED_VIEW' THEN 'materialized view'
    WHEN 'METRIC_VIEW' THEN 'metric view'
    ELSE lower(table_type)
  END AS type,
  coalesce(comment, '') AS description,
  date_format(last_altered, 'yyyy-MM-dd HH:mm') AS last_updated
FROM workspace.information_schema.tables
WHERE table_schema IN ('bronze', 'silver', 'gold')
  -- hide pipeline internals; left() instead of startswith/LIKE because '_' is a LIKE wildcard
  AND left(table_name, 2) <> '__'
  AND left(table_name, 10) <> 'event_log_'
ORDER BY CASE table_schema WHEN 'bronze' THEN 1 WHEN 'silver' THEN 2 ELSE 3 END, table_name;
