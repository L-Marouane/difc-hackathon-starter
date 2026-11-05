-- GOLD: business-ready tables. These names and columns are the contract the app and Genie expect.

-- One row per customer per month they were paying (plus the month they churned).

CREATE OR REFRESH MATERIALIZED VIEW gold.mrr_monthly
COMMENT "Customer x month MRR in AED with movement type (new, expansion, contraction, churn, reactivation, flat). Grain: customer_id + month. Always group by month when summing MRR."
AS
WITH bounds AS (
  SELECT trunc(max(effective_at), 'MM') AS last_month FROM silver.subscription_events
),
first_seen AS (
  SELECT customer_id, trunc(min(effective_at), 'MM') AS first_month FROM silver.subscription_events GROUP BY customer_id
),
spine AS (
  SELECT f.customer_id, m.month
  FROM first_seen f CROSS JOIN bounds b
  LATERAL VIEW explode(sequence(f.first_month, b.last_month, INTERVAL 1 MONTH)) m AS month
),
state AS (  -- subscription state in force at the end of each month
  SELECT s.customer_id, s.month,
         max_by(e.mrr_aed, e.effective_at) AS mrr_aed,
         max_by(e.plan_name, e.effective_at) AS plan_name,
         max_by(e.seats, e.effective_at) AS seats
  FROM spine s
  JOIN silver.subscription_events e
    ON e.customer_id = s.customer_id AND e.effective_at < add_months(s.month, 1)
  GROUP BY s.customer_id, s.month
),
moves AS (
  SELECT *,
         coalesce(lag(mrr_aed) OVER (PARTITION BY customer_id ORDER BY month), 0) AS prev_mrr_aed,
         row_number() OVER (PARTITION BY customer_id ORDER BY month) AS month_index
  FROM state
)
SELECT
  m.month,
  m.customer_id,
  c.company_name,
  c.country,
  c.industry,
  c.company_size,
  c.acquisition_channel,
  trunc(c.signup_date, 'MM') AS signup_cohort,
  m.plan_name,
  m.seats,
  round(m.mrr_aed, 2) AS mrr_aed,
  round(m.prev_mrr_aed, 2) AS prev_mrr_aed,
  m.mrr_aed > 0 AS is_active,
  CASE
    WHEN m.prev_mrr_aed = 0 AND m.mrr_aed > 0 AND m.month_index = 1 THEN 'new'
    WHEN m.prev_mrr_aed = 0 AND m.mrr_aed > 0 THEN 'reactivation'
    WHEN m.prev_mrr_aed > 0 AND m.mrr_aed = 0 THEN 'churn'
    WHEN m.mrr_aed > m.prev_mrr_aed THEN 'expansion'
    WHEN m.mrr_aed < m.prev_mrr_aed THEN 'contraction'
    ELSE 'flat'
  END AS movement,
  CASE WHEN m.prev_mrr_aed = 0 AND m.mrr_aed > 0 AND m.month_index = 1 THEN m.mrr_aed ELSE 0 END AS new_mrr_aed,
  CASE WHEN m.prev_mrr_aed = 0 AND m.mrr_aed > 0 AND m.month_index > 1 THEN m.mrr_aed ELSE 0 END AS reactivation_mrr_aed,
  CASE WHEN m.prev_mrr_aed > 0 AND m.mrr_aed > m.prev_mrr_aed THEN m.mrr_aed - m.prev_mrr_aed ELSE 0 END AS expansion_mrr_aed,
  CASE WHEN m.mrr_aed > 0 AND m.mrr_aed < m.prev_mrr_aed THEN m.prev_mrr_aed - m.mrr_aed ELSE 0 END AS contraction_mrr_aed,
  CASE WHEN m.prev_mrr_aed > 0 AND m.mrr_aed = 0 THEN m.prev_mrr_aed ELSE 0 END AS churned_mrr_aed
FROM moves m
JOIN silver.customers c ON c.customer_id = m.customer_id
WHERE m.mrr_aed > 0 OR m.prev_mrr_aed > 0;

-- One row per customer: who they are, what they pay, how they use the product, and how risky they look today.

CREATE OR REFRESH MATERIALIZED VIEW gold.customer_360
COMMENT "One row per customer with current plan, MRR, usage trend, payment health, support load and a rule-based churn risk level."
AS
WITH as_of AS (
  SELECT CAST(max(event_ts) AS DATE) AS as_of_date FROM silver.product_events
),
current_sub AS (
  SELECT customer_id,
         max_by(event_type, effective_at) AS last_event_type,
         max_by(effective_at, effective_at) AS last_event_at,
         max_by(plan_name, effective_at) AS plan_name,
         max_by(seats, effective_at) AS seats,
         max_by(billing_cycle, effective_at) AS billing_cycle,
         max_by(mrr_aed, effective_at) AS mrr_aed
  FROM silver.subscription_events GROUP BY customer_id
),
usage AS (
  SELECT e.customer_id,
         count_if(e.event_ts >= date_sub(a.as_of_date, 29)) AS events_last_30d,
         count_if(e.event_ts >= date_sub(a.as_of_date, 59) AND e.event_ts < date_sub(a.as_of_date, 29)) AS events_prev_30d,
         count_if(e.event_name = 'payment_link_failed' AND e.event_ts >= date_sub(a.as_of_date, 89)) AS payment_link_failures_90d,
         max(e.event_ts) AS last_seen_at
  FROM silver.product_events e CROSS JOIN as_of a
  GROUP BY e.customer_id
),
activation AS (
  SELECT e.customer_id, min(e.event_ts) AS first_integration_at, min_by(e.integration, e.event_ts) AS integration
  FROM silver.product_events e WHERE e.event_name = 'integration_connected' GROUP BY e.customer_id
),
billing AS (
  SELECT i.customer_id,
         count_if(i.status = 'failed' AND i.issued_at >= date_sub(a.as_of_date, 89)) AS failed_invoices_90d,
         sum(CASE WHEN i.status IN ('failed', 'overdue', 'pending') THEN i.amount_aed ELSE 0 END) AS unpaid_amount_aed
  FROM silver.invoices i CROSS JOIN as_of a
  GROUP BY i.customer_id
),
support AS (
  SELECT t.customer_id,
         count_if(t.created_at >= date_sub(a.as_of_date, 89)) AS tickets_90d,
         count_if(t.status IN ('open', 'pending')) AS open_tickets,
         count_if(t.topic = 'cancellation' AND t.created_at >= date_sub(a.as_of_date, 89)) AS cancellation_tickets_90d,
         max_by(t.subject, t.created_at) AS last_ticket_subject
  FROM silver.support_tickets t CROSS JOIN as_of a
  GROUP BY t.customer_id
),
base AS (
  SELECT
    c.customer_id, c.company_name, c.industry, c.country, c.city, c.company_size, c.acquisition_channel,
    c.account_manager, c.signup_date,
    CASE WHEN s.last_event_type = 'churn' THEN 'churned' ELSE 'active' END AS status,
    CASE WHEN s.last_event_type = 'churn' THEN CAST(s.last_event_at AS DATE) END AS churn_date,
    s.plan_name, s.seats, s.billing_cycle,
    CASE WHEN s.last_event_type = 'churn' THEN 0 ELSE round(s.mrr_aed, 2) END AS mrr_aed,
    CAST(months_between(a.as_of_date, c.signup_date) AS INT) AS tenure_months,
    coalesce(act.first_integration_at <= c.signup_date + INTERVAL 14 DAYS, false) AS activated_14d,
    act.integration,
    coalesce(u.events_last_30d, 0) AS events_last_30d,
    coalesce(u.events_prev_30d, 0) AS events_prev_30d,
    round(100 * (coalesce(u.events_last_30d, 0) - u.events_prev_30d) / nullif(u.events_prev_30d, 0), 1) AS usage_change_pct,
    coalesce(u.payment_link_failures_90d, 0) AS payment_link_failures_90d,
    u.last_seen_at,
    coalesce(b.failed_invoices_90d, 0) AS failed_invoices_90d,
    round(coalesce(b.unpaid_amount_aed, 0), 2) AS unpaid_amount_aed,
    coalesce(t.tickets_90d, 0) AS tickets_90d,
    coalesce(t.open_tickets, 0) AS open_tickets,
    coalesce(t.cancellation_tickets_90d, 0) AS cancellation_tickets_90d,
    t.last_ticket_subject,
    a.as_of_date
  FROM silver.customers c
  JOIN current_sub s ON s.customer_id = c.customer_id
  CROSS JOIN as_of a
  LEFT JOIN usage u ON u.customer_id = c.customer_id
  LEFT JOIN activation act ON act.customer_id = c.customer_id
  LEFT JOIN billing b ON b.customer_id = c.customer_id
  LEFT JOIN support t ON t.customer_id = c.customer_id
)
SELECT *,
  CASE
    WHEN status = 'churned' THEN NULL
    WHEN (events_prev_30d >= 5 AND usage_change_pct <= -50) OR failed_invoices_90d >= 2 OR cancellation_tickets_90d > 0 THEN 'high'
    WHEN usage_change_pct <= -30 OR failed_invoices_90d >= 1 OR open_tickets >= 2 THEN 'medium'
    ELSE 'low'
  END AS risk_level,
  CASE
    WHEN status = 'churned' THEN NULL
    ELSE concat_ws('; ',
      CASE WHEN events_prev_30d >= 5 AND usage_change_pct <= -30 THEN concat('usage down ', CAST(-usage_change_pct AS INT), '% vs previous 30 days') END,
      CASE WHEN failed_invoices_90d > 0 THEN concat(failed_invoices_90d, ' failed invoice(s) in 90 days') END,
      CASE WHEN cancellation_tickets_90d > 0 THEN 'raised a cancellation ticket' END,
      CASE WHEN open_tickets >= 2 THEN concat(open_tickets, ' open tickets') END)
  END AS risk_reasons
FROM base;

-- Acquisition economics per channel per month.

CREATE OR REFRESH MATERIALIZED VIEW gold.acquisition_monthly
COMMENT "Marketing spend, leads, signups, activated signups and revenue collected to date from that signup cohort, by acquisition channel and signup month."
AS
WITH signups AS (
  SELECT trunc(signup_date, 'MM') AS month, acquisition_channel,
         count(*) AS signups,
         count_if(activated_14d) AS activated_signups,
         count_if(status = 'churned') AS churned_to_date
  FROM gold.customer_360
  GROUP BY ALL
),
revenue AS (  -- revenue collected to date from each signup cohort, the basis for payback and LTV:CAC
  SELECT signup_cohort AS month, acquisition_channel, sum(mrr_aed) AS revenue_to_date_aed
  FROM gold.mrr_monthly
  GROUP BY ALL
)
SELECT
  coalesce(s.month, m.month) AS month,
  coalesce(s.acquisition_channel, m.acquisition_channel) AS acquisition_channel,
  coalesce(m.spend_aed, 0) AS spend_aed,
  m.leads,
  m.clicks,
  coalesce(s.signups, 0) AS signups,
  coalesce(s.activated_signups, 0) AS activated_signups,
  coalesce(s.churned_to_date, 0) AS churned_to_date,
  round(coalesce(r.revenue_to_date_aed, 0), 2) AS revenue_to_date_aed
FROM signups s
FULL OUTER JOIN silver.marketing_spend m
  ON m.month = s.month AND m.acquisition_channel = s.acquisition_channel
LEFT JOIN revenue r
  ON r.month = coalesce(s.month, m.month) AND r.acquisition_channel = coalesce(s.acquisition_channel, m.acquisition_channel);

-- Support tickets enriched with customer context.

CREATE OR REFRESH MATERIALIZED VIEW gold.support_tickets
COMMENT "Support tickets with topic, resolution time and customer attributes."
AS SELECT
  t.ticket_id, t.customer_id, c.company_name, c.country, c.company_size, c.acquisition_channel,
  t.created_at, trunc(t.created_at, 'MM') AS created_month, t.resolved_at,
  round((unix_timestamp(t.resolved_at) - unix_timestamp(t.created_at)) / 3600, 1) AS resolution_hours,
  t.channel, t.priority, t.status, t.topic, t.subject, t.description, t.first_response_minutes, t.csat_score
FROM silver.support_tickets t
JOIN silver.customers c ON c.customer_id = t.customer_id;
