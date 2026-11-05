-- Headline KPIs for the latest month in the data
WITH latest AS (
  SELECT max(month) AS m FROM workspace.gold.mrr_monthly
),
rev AS (
  SELECT
    sum(CASE WHEN r.month = l.m THEN r.mrr_aed ELSE 0 END) AS mrr_aed,
    sum(CASE WHEN r.month = add_months(l.m, -1) THEN r.mrr_aed ELSE 0 END) AS prev_mrr_aed,
    count(DISTINCT CASE WHEN r.month = l.m AND r.is_active THEN r.customer_id END) AS active_customers,
    count(DISTINCT CASE WHEN r.month = l.m AND r.movement = 'churn' THEN r.customer_id END) AS churned_customers
  FROM workspace.gold.mrr_monthly r
  CROSS JOIN latest l
),
risk AS (
  SELECT
    count_if(status = 'active' AND risk_level = 'high') AS high_risk_accounts,
    coalesce(sum(CASE WHEN status = 'active' AND risk_level = 'high' THEN mrr_aed END), 0) AS mrr_at_risk_aed,
    max(as_of_date) AS as_of_date
  FROM workspace.gold.customer_360
)
SELECT
  date_format(l.m, 'MMMM yyyy') AS latest_month,
  CAST(risk.as_of_date AS STRING) AS as_of_date,
  round(rev.mrr_aed, 0) AS mrr_aed,
  round(100 * (rev.mrr_aed - rev.prev_mrr_aed) / nullif(rev.prev_mrr_aed, 0), 1) AS mrr_growth_pct,
  rev.active_customers,
  rev.churned_customers,
  risk.high_risk_accounts,
  round(risk.mrr_at_risk_aed, 0) AS mrr_at_risk_aed
FROM rev CROSS JOIN risk CROSS JOIN latest l;
