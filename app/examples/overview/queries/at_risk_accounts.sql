-- @param country STRING
-- Active high-risk accounts, biggest first. country = 'all' returns every country.
SELECT
  company_name,
  country,
  plan_name AS plan,
  round(mrr_aed, 0) AS mrr_aed,
  usage_change_pct,
  failed_invoices_90d,
  risk_reasons,
  account_manager,
  customer_id
FROM workspace.gold.customer_360
WHERE status = 'active'
  AND risk_level = 'high'
  AND (:country = 'all' OR country = :country)
ORDER BY mrr_aed DESC
LIMIT 50;
