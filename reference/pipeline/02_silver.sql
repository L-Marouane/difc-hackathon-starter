-- SILVER: clean, type, deduplicate, standardise. Data quality rules are enforced with expectations.

CREATE OR REFRESH MATERIALIZED VIEW silver.fx_rates
COMMENT "Monthly FX rate to AED per currency."
AS SELECT DISTINCT
  to_date(substr(CAST(month AS STRING), 1, 7), 'yyyy-MM') AS month,  -- CSV inference may already make month a DATE
  upper(trim(currency)) AS currency,
  CAST(rate_to_aed AS DOUBLE) AS rate_to_aed
FROM bronze.fx_rates;

CREATE OR REFRESH MATERIALIZED VIEW silver.customers (
  CONSTRAINT valid_customer_id EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_signup_date EXPECT (signup_date IS NOT NULL),
  CONSTRAINT known_country EXPECT (country IN ('United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Bahrain', 'Oman', 'Kuwait'))
)
COMMENT "One row per real customer: latest CRM record, test accounts removed, country and dates standardised."
AS
WITH ranked AS (
  SELECT *, row_number() OVER (PARTITION BY customer_id ORDER BY to_timestamp(last_modified) DESC, source_file DESC) AS rn
  FROM bronze.crm_customers
)
SELECT
  customer_id,
  trim(company_name) AS company_name,
  coalesce(industry, 'Unknown') AS industry,
  CASE
    WHEN upper(regexp_replace(country, '[^A-Za-z]', '')) IN ('UNITEDARABEMIRATES', 'UAE', 'AE') THEN 'United Arab Emirates'
    WHEN upper(regexp_replace(country, '[^A-Za-z]', '')) IN ('SAUDIARABIA', 'KSA', 'SA', 'KINGDOMOFSAUDIARABIA') THEN 'Saudi Arabia'
    WHEN upper(country) IN ('QATAR', 'QA') THEN 'Qatar'
    WHEN upper(country) IN ('BAHRAIN', 'BH') THEN 'Bahrain'
    WHEN upper(country) IN ('OMAN', 'OM') THEN 'Oman'
    WHEN upper(country) IN ('KUWAIT', 'KW') THEN 'Kuwait'
    ELSE country
  END AS country,
  city,
  company_size,
  acquisition_channel,
  coalesce(try_to_date(signup_date, 'yyyy-MM-dd'), try_to_date(signup_date, 'dd/MM/yyyy'), try_to_date(signup_date, 'MMM dd, yyyy')) AS signup_date,
  account_manager,
  contact_email,
  to_timestamp(last_modified) AS last_modified
FROM ranked
WHERE rn = 1
  AND company_name NOT LIKE 'TEST ACCOUNT%'
  AND contact_email NOT LIKE '%@falak.io';

CREATE OR REFRESH MATERIALIZED VIEW silver.subscription_events (
  CONSTRAINT valid_event_type EXPECT (event_type IN ('new', 'upgrade', 'downgrade', 'seat_change', 'churn', 'reactivation')),
  CONSTRAINT non_negative_mrr EXPECT (mrr >= 0),
  CONSTRAINT has_fx_rate EXPECT (mrr_aed IS NOT NULL)
)
COMMENT "Subscription lifecycle events, plan struct flattened, MRR converted to AED."
AS SELECT
  e.event_id,
  e.customer_id,
  e.event_type,
  CAST(e.effective_at AS TIMESTAMP) AS effective_at,
  e.billing_cycle,
  e.plan.name AS plan_name,
  CAST(e.plan.seats AS INT) AS seats,
  CAST(e.plan.mrr AS DOUBLE) AS mrr,
  e.plan.currency AS currency,
  round(CAST(e.plan.mrr AS DOUBLE) * fx.rate_to_aed, 2) AS mrr_aed
FROM bronze.subscription_events e
JOIN silver.customers c ON c.customer_id = e.customer_id            -- drops QA test accounts
LEFT JOIN silver.fx_rates fx
  ON fx.currency = e.plan.currency AND fx.month = trunc(CAST(e.effective_at AS TIMESTAMP), 'MM');

CREATE OR REFRESH MATERIALIZED VIEW silver.invoices (
  CONSTRAINT valid_amount EXPECT (amount > 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_status EXPECT (status IN ('paid', 'failed', 'overdue', 'pending', 'refunded')),
  CONSTRAINT has_fx_rate EXPECT (amount_aed IS NOT NULL)
)
COMMENT "Invoices with normalised status, numeric amounts and AED conversion."
AS SELECT
  i.invoice_id,
  i.customer_id,
  CAST(i.issued_at AS TIMESTAMP) AS issued_at,
  to_date(i.due_date) AS due_date,
  i.plan AS plan_name,
  CAST(i.amount AS DOUBLE) AS amount,
  i.currency,
  round(CAST(i.amount AS DOUBLE) * fx.rate_to_aed, 2) AS amount_aed,
  lower(trim(i.status)) AS status,
  CAST(i.payment_attempts AS INT) AS payment_attempts,
  CAST(i.paid_at AS TIMESTAMP) AS paid_at,
  i.payment_method
FROM bronze.invoices i
JOIN silver.customers c ON c.customer_id = i.customer_id
LEFT JOIN silver.fx_rates fx
  ON fx.currency = i.currency AND fx.month = trunc(CAST(i.issued_at AS TIMESTAMP), 'MM');

CREATE OR REFRESH MATERIALIZED VIEW silver.product_events (
  CONSTRAINT valid_ts EXPECT (event_ts IS NOT NULL) ON VIOLATION DROP ROW
)
COMMENT "Product usage events, deduplicated on event_id, timestamps parsed, context flattened."
AS SELECT
  event_id,
  customer_id,
  user_id,
  event_name,
  CAST(event_ts AS TIMESTAMP) AS event_ts,
  context.platform AS platform,
  context.app_version AS app_version,
  context.locale AS locale,
  properties.amount AS amount,
  properties.integration AS integration,
  properties.error_code AS error_code,
  properties.report AS report_type
FROM bronze.product_events
QUALIFY row_number() OVER (PARTITION BY event_id ORDER BY ingested_at) = 1;

CREATE OR REFRESH MATERIALIZED VIEW silver.support_tickets
COMMENT "Support tickets with parsed timestamps, normalised status and a rule-based topic."
AS SELECT
  ticket_id,
  customer_id,
  CAST(created_at AS TIMESTAMP) AS created_at,
  CAST(resolved_at AS TIMESTAMP) AS resolved_at,
  channel,
  priority,
  subject,
  description,
  CASE WHEN lower(status) IN ('resolved', 'closed') THEN 'closed' ELSE lower(status) END AS status,
  first_response_minutes,
  CAST(csat_score AS INT) AS csat_score,
  agent_category AS agent_category_raw,
  CASE
    WHEN lower(subject) RLIKE 'cancel|alternatives|downgrade or cancel' OR subject LIKE '%إلغاء%' THEN 'cancellation'
    WHEN lower(subject) RLIKE 'arabic invoice|whatsapp|multi-currency' OR subject LIKE '%ميزة%' THEN 'feature_request'
    WHEN lower(subject) RLIKE 'import|template|adding my team' OR subject LIKE '%شعار%' THEN 'onboarding'
    WHEN lower(subject) RLIKE 'payment link|declined|stuck in processing' OR subject LIKE '%الدفع%' THEN 'payment_failure'
    WHEN lower(subject) RLIKE 'e-invoic|zatca' OR subject LIKE '%فاتورة%' THEN 'e_invoicing'
    WHEN lower(subject) RLIKE 'sync|connection|not showing in' THEN 'integration_sync'
    WHEN lower(subject) RLIKE 'charged|seats|tax invoice|annual billing' THEN 'billing_question'
    ELSE 'how_to'
  END AS topic
FROM bronze.support_tickets
WHERE customer_id NOT LIKE 'C-9%';

CREATE OR REFRESH MATERIALIZED VIEW silver.marketing_spend
COMMENT "Monthly marketing spend mapped to CRM acquisition channel names."
AS SELECT
  to_date(substr(CAST(month AS STRING), 1, 7), 'yyyy-MM') AS month,  -- CSV inference may already make month a DATE
  CASE channel
    WHEN 'paid_social' THEN 'Paid Social'
    WHEN 'google_ads' THEN 'Google Ads'
    WHEN 'seo_content' THEN 'Organic'
    WHEN 'referral_program' THEN 'Referral'
    WHEN 'bank_partnership' THEN 'Partner Bank'
    WHEN 'events' THEN 'Events'
  END AS acquisition_channel,
  CAST(spend_aed AS DOUBLE) AS spend_aed,
  CAST(impressions AS BIGINT) AS impressions,
  CAST(clicks AS BIGINT) AS clicks,
  CAST(leads AS BIGINT) AS leads
FROM bronze.marketing_spend;
