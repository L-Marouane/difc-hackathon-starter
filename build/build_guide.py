"""Builds 01_Hackathon_Guide.py: context, medallion + SDP with Genie Code prompts, metric views, Genie Agent.
Run: python3 build/build_guide.py   (slides come from build/slides.py, the DGE workshop slide engine)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from slides import Notebook, Slide

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/01_Hackathon_Guide.py"

# ------------------------------------------------------------------------------------------------ prompts
GENIE_CODE_INSTRUCTIONS = open(f"{ROOT}/guides/genie_code_instructions.md").read().strip()

PROMPT_BRONZE = """In this pipeline, create the file 01_bronze.sql with one streaming table per source.
Use STREAM read_files on these folders of /Volumes/workspace/raw/landing/ :

- bronze.crm_customers        <- crm/                           (format csv, header true)
- bronze.subscription_events  <- billing/subscription_events/   (format json)
- bronze.invoices             <- billing/invoices/              (format json, schemaHints 'amount STRING')
- bronze.product_events       <- product_events/                (format json)
- bronze.support_tickets      <- support/tickets/               (format json)
- bronze.marketing_spend      <- marketing/                     (format csv, header true)
- bronze.fx_rates             <- reference/                     (format csv, header true)

Keep every column as delivered, do not clean anything. Add two columns to each table:
source_file (from _metadata.file_path) and ingested_at (current_timestamp()).
Add a one-line COMMENT on each table describing the source system."""

PROMPT_DETECTIVE = """Profile the 7 bronze tables and list every data quality problem you find:
duplicates, test or fake records, inconsistent values, mixed date or timestamp formats,
wrong types, nested fields, codes that do not match between tables.
Answer with a table: bronze table | problem | example value | how to fix it in silver."""

PROMPT_SILVER = """Create the file 02_silver.sql with one MATERIALIZED VIEW per entity, in the silver schema.

1. silver.fx_rates: month (DATE), currency (upper case), rate_to_aed (DOUBLE).
   The CSV month may already be inferred as a DATE: use to_date(substr(CAST(month AS STRING), 1, 7), 'yyyy-MM').

2. silver.customers: one row per customer_id, keeping the row with the latest last_modified.
   - remove QA test accounts: company_name starting with 'TEST ACCOUNT' or contact_email ending with '@falak.io'
   - trim company_name; industry NULL becomes 'Unknown'
   - country to full names: UAE, U.A.E., AE, uae -> United Arab Emirates; KSA, SA, Kingdom of Saudi Arabia -> Saudi Arabia;
     QA -> Qatar; BH -> Bahrain; OM -> Oman; KW -> Kuwait
   - signup_date as DATE from three formats: yyyy-MM-dd, dd/MM/yyyy and MMM dd, yyyy (use try_to_date + coalesce)
   - expectations: customer_id IS NOT NULL (drop row), signup_date IS NOT NULL, country in the 6 full names

3. silver.subscription_events: flatten the plan struct into plan_name, seats (INT), mrr (DOUBLE), currency;
   effective_at as TIMESTAMP; mrr_aed = mrr x rate_to_aed, joining silver.fx_rates on currency and the month of effective_at.
   Inner join silver.customers to keep real customers only.
   Expectations: event_type in (new, upgrade, downgrade, seat_change, churn, reactivation), mrr >= 0, mrr_aed IS NOT NULL.

4. silver.invoices: issued_at and paid_at as TIMESTAMP, due_date as DATE, amount as DOUBLE (it is sometimes a string),
   status lower-cased and trimmed, amount_aed via silver.fx_rates (month of issued_at). Real customers only.
   Expectations: amount > 0 (drop row), status in (paid, failed, overdue, pending, refunded), amount_aed IS NOT NULL.

5. silver.product_events: deduplicate on event_id (QUALIFY row_number() OVER (PARTITION BY event_id ORDER BY ingested_at) = 1),
   event_ts as TIMESTAMP (two formats exist, CAST handles both), flatten context into platform, app_version, locale and
   properties into amount, integration, error_code, report_type. Expectation: event_ts IS NOT NULL (drop row).

6. silver.support_tickets: created_at and resolved_at as TIMESTAMP, status 'resolved' or 'closed' (any case) -> 'closed',
   otherwise lower-cased; csat_score INT; keep agent_category as agent_category_raw; exclude customer_id starting with 'C-9'.
   Add a topic column from the subject, checked in this order (subjects can be Arabic):
   cancellation (cancel, alternatives, or Arabic إلغاء) ; feature_request (arabic invoice, whatsapp, multi-currency, or ميزة) ;
   onboarding (import, template, adding my team, or شعار) ; payment_failure (payment link, declined, stuck in processing, or الدفع) ;
   e_invoicing (e-invoic, zatca, or فاتورة) ; integration_sync (sync, connection, not showing in) ;
   billing_question (charged, seats, tax invoice, annual billing) ; otherwise how_to.

7. silver.marketing_spend: month as DATE (same trick as fx_rates), map channel codes to CRM names:
   paid_social -> Paid Social, google_ads -> Google Ads, seo_content -> Organic, referral_program -> Referral,
   bank_partnership -> Partner Bank, events -> Events. spend_aed DOUBLE, impressions, clicks and leads BIGINT.

Add a COMMENT to every table."""

PROMPT_GOLD = """Create the file 03_gold.sql with these MATERIALIZED VIEWS in the gold schema.
Keep the names and columns exactly: the app and Genie use them.

1. gold.mrr_monthly: one row per customer per month.
   - month spine: from the month of each customer's first subscription event to the latest month in silver.subscription_events
   - state at month end = the latest subscription event with effective_at before the next month (max_by): mrr_aed, plan_name, seats
   - prev_mrr_aed = previous month's mrr_aed (0 if none); is_active = mrr_aed > 0
   - movement: new (first month, prev 0), reactivation (prev 0, not first month), churn (prev > 0, now 0),
     expansion (mrr up), contraction (mrr down, still > 0), flat
   - new_mrr_aed, reactivation_mrr_aed, expansion_mrr_aed, contraction_mrr_aed, churned_mrr_aed (the MRR amount of that movement)
   - add company_name, country, industry, company_size, acquisition_channel and signup_cohort (signup month) from silver.customers
   - keep only rows where mrr_aed > 0 or prev_mrr_aed > 0

2. gold.customer_360: one row per customer. as_of_date = CAST(max(event_ts) AS DATE) from silver.product_events ("today").
   - profile: customer_id, company_name, industry, country, city, company_size, acquisition_channel, account_manager, signup_date
   - from the latest subscription event: status ('churned' if it is a churn, else 'active'), churn_date, plan_name, seats,
     billing_cycle, mrr_aed (0 if churned); tenure_months = months between signup_date and as_of_date
   - activated_14d: an integration_connected event within 14 days of signup_date; integration = the first one connected
   - events_last_30d (event_ts >= as_of_date - 29 days), events_prev_30d (the 30 days before that),
     usage_change_pct = 100 x (last - prev) / prev, payment_link_failures_90d
   - failed_invoices_90d (status failed, issued in the last 90 days), unpaid_amount_aed (failed, overdue, pending)
   - tickets_90d, open_tickets (open or pending), cancellation_tickets_90d, last_ticket_subject
   - risk_level, for active customers only:
     high   = (events_prev_30d >= 5 and usage_change_pct <= -50) or failed_invoices_90d >= 2 or cancellation_tickets_90d > 0
     medium = usage_change_pct <= -30 or failed_invoices_90d >= 1 or open_tickets >= 2
     low    = everything else
   - risk_reasons: a readable sentence, for example 'usage down 61% vs previous 30 days; 2 failed invoice(s) in 90 days'

3. gold.acquisition_monthly: month x acquisition_channel, full outer join of
   signups from gold.customer_360 (signups, activated_signups, churned_to_date, by signup month and channel) and
   silver.marketing_spend (spend_aed, leads, clicks), plus revenue_to_date_aed = sum of mrr_aed in gold.mrr_monthly
   for that signup_cohort and channel.

4. gold.support_tickets: silver.support_tickets joined with silver.customers (company_name, country, company_size,
   acquisition_channel), plus created_month and resolution_hours.

Add a COMMENT to every table, and column comments on the non-obvious columns."""

PROMPT_MV_REVENUE = """Create a Unity Catalog metric view workspace.gold.revenue_metrics on workspace.gold.mrr_monthly
(CREATE OR REPLACE VIEW ... WITH METRICS LANGUAGE YAML, version 1.1), and run it.

Dimensions: Month, Country, Industry, Company Size, Acquisition Channel, Plan (plan_name), Signup Cohort, Movement.
Measures:
- MRR = SUM(mrr_aed)
- Active Customers = COUNT(DISTINCT customer_id) where is_active
- ARPA = MRR / Active Customers
- New MRR, Expansion MRR, Contraction MRR, Churned MRR, Reactivation MRR = SUM of the matching column
- Net New MRR = new + expansion + reactivation - contraction - churned
- Churned Customers = COUNT(DISTINCT customer_id) where movement = 'churn'
- Logo Churn Rate = Churned Customers / COUNT(DISTINCT customer_id) where prev_mrr_aed > 0
- Net Revenue Retention = SUM(mrr_aed where prev_mrr_aed > 0) / SUM(prev_mrr_aed)

Add a view comment saying MRR is a monthly snapshot and must always be sliced by Month.
Add synonyms: MRR -> monthly recurring revenue, revenue; Logo Churn Rate -> churn rate; Net Revenue Retention -> NRR;
Acquisition Channel -> channel, marketing channel."""

PROMPT_MV_ACQ = """Create a metric view workspace.gold.acquisition_metrics on workspace.gold.acquisition_monthly, and run it.

Dimensions: Month, Acquisition Channel.
Measures:
- Marketing Spend = SUM(spend_aed); Leads = SUM(leads); Signups = SUM(signups)
- CAC = Marketing Spend / Signups; Cost per Lead = Marketing Spend / Leads
- Activation Rate = SUM(activated_signups) / Signups
- Churned Share = SUM(churned_to_date) / Signups
- Revenue to Date = SUM(revenue_to_date_aed)
- Return on Spend = Revenue to Date / Marketing Spend
Synonyms: Return on Spend -> payback, ROAS, LTV to CAC; CAC -> customer acquisition cost; Marketing Spend -> spend, ad spend."""

GENIE_DESCRIPTION = """Ask anything about Falak's business: revenue and MRR, churn and at-risk accounts, marketing efficiency by channel, and support tickets. Data is up to the end of October 2026, money in AED."""

GENIE_INSTRUCTIONS = """You are Falak's business analyst. Falak sells invoicing and payment-link software to SMEs in the GCC.
- Money is in AED. Round to whole AED and use thousands separators.
- "Today" is the as_of_date column in customer_360 (end of October 2026). "Last month" = October 2026.
- MRR is a monthly snapshot: always filter or group revenue_metrics by Month. Never sum MRR across months.
- "Churn rate" means the Logo Churn Rate measure, per month. "Customers" means active paying customers.
- "At risk" means customer_360.risk_level = 'high' and status = 'active'. Show risk_reasons when listing them.
- For questions about marketing efficiency, CAC, payback or LTV, use acquisition_metrics. Return on Spend below 1.3 is poor.
- KSA = Saudi Arabia. UAE = United Arab Emirates.
- When you list customers, show company_name, country, plan_name, mrr_aed and account_manager.
- For "what happened" questions about a period or a country, investigate like an analyst: compare churned customers, failed invoices (customer_360) and support ticket topics (support_tickets) with the months before, not only MRR."""

GENIE_QUESTIONS = """What is our MRR trend over the last 12 months?
Which accounts are at risk right now and how much MRR is at stake?
Which acquisition channel gives the best return on marketing spend?
What happened in Saudi Arabia in summer 2026?
Do customers who connect an integration early churn less?"""

# ------------------------------------------------------------------------------------------------ notebook
nb = Notebook()

# ---- 0. title
nb.slide(Slide()
    .banner("Falak Hackathon Guide", "From raw files to an AI-powered app in about an hour", icon="F")
    .callout(eyebrow="Do this first", icon="!", kind="caution",
             title="Run 00_Setup_Data now, then read on while it works (about 5 minutes)",
             text="It lands Falak's raw data in your workspace and deploys your starter app <code>falak-app</code>.")
    .flow([("Context", "Falak and its data", "teal"), ("Pipeline", "Bronze, silver, gold", "blue"),
           ("Metric views", "One definition per KPI", "green"), ("Genie Agent", "Ask the data", "amber"),
           ("App", "Claude Code", "coral")]))

# ---- 1. context
nb.slide(Slide()
    .header("Meet Falak", "A fictional Dubai startup: invoicing and payment links for SMEs across the GCC", eyebrow="The context")
    .cards([{"stat": "2,700", "label": "paying SME customers", "accent": "blue"},
            {"stat": "2.0M AED", "label": "monthly recurring revenue", "accent": "green"},
            {"stat": "6", "label": "GCC countries, KSA launched Sep 2024", "accent": "amber"},
            {"stat": "3 plans", "label": "Starter, Growth, Scale, billed in AED, SAR or USD", "accent": "coral"}], kind="stat")
    .callout(eyebrow="The situation", kind="info",
             title="Falak grew fast. The founders feel that something is off, but every team tells a different story.",
             items=["Marketing doubled the paid social budget in mid-2025. Was it worth it?",
                    "Churn jumped in late summer. Was it a one-off or a pattern?",
                    "The biggest accounts look fine on the CRM. Are they?"])
    .band("Your mission: find the problems hiding in the data, and build the tool the founders need to act on them.", accent="coral"))

nb.slide(Slide()
    .header("The raw data", "Six source systems, delivered as files in a Unity Catalog volume: /Volumes/workspace/raw/landing/", eyebrow="What you start with")
    .table(["Source system", "Folder", "Format", "Rows", "What is inside"], [
        ["CRM export", "crm/", "CSV", "~4.1k", "Customers: company, industry, country, size, acquisition channel, account manager"],
        ["Billing: subscriptions", "billing/subscription_events/", "JSON, nested <code>plan</code>", "~8.5k", "New, upgrade, downgrade, seat change, churn, reactivation, with MRR"],
        ["Billing: invoices", "billing/invoices/", "JSON", "~34k", "Monthly invoices, status, payment method, attempts"],
        ["Product analytics", "product_events/", "JSON, nested <code>context</code>", "~1.0M", "Logins, invoices created, payment links sent or failed, integrations"],
        ["Support desk", "support/tickets/", "JSON, free text", "~5.3k", "Subject and description in English and Arabic, CSAT"],
        ["Marketing", "marketing/", "CSV", "204", "Monthly spend, clicks and leads per channel"],
        ["Finance", "reference/", "CSV", "105", "Monthly FX rates to AED"],
    ], mono_cols=(1,))
    .callout(eyebrow="Heads up", kind="caution", icon="!",
             text="The data is messy on purpose, like real exports: duplicates, QA test accounts, a country spelled five ways, "
                  "three date formats, three currencies, statuses in mixed case. Cleaning it is part of the job."))

nb.slide(Slide()
    .header("What you will build", "Four steps, each with a copy-paste prompt. The app is already deployed and waiting.", eyebrow="The plan")
    .flow([("Raw files", "volume", "teal"), ("Bronze", "ingest as-is", "amber"), ("Silver", "clean and conform", "blue"),
           ("Gold", "business tables", "green"), ("Metric views", "governed KPIs", "green"), ("Genie + App", "answers and actions", "coral")])
    .table(["Step", "You build", "Tool", "Time"], [
        ["1", "A Lakeflow Spark Declarative Pipeline: 7 bronze, 7 silver, 4 gold tables", "Genie Code in the Lakeflow Pipelines Editor", "25 min"],
        ["2", "Two metric views: revenue and acquisition", "Genie Code in the SQL editor", "10 min"],
        ["3", "A Genie Agent that answers business questions correctly", "Genie", "10 min"],
        ["4", "Your product on top of <code>falak-app</code>", "Claude Code on your laptop (<code>guides/4_App_with_Claude.md</code>)", "25 min"],
    ])
    .callout(eyebrow="Behind schedule?", kind="success",
             text="Run <code>99_Catch_Up</code>: it builds the reference pipeline and the metric views in about 3 minutes. Then jump to step 3."))

# ---- 2. medallion
nb.slide(Slide()
    .header("The medallion architecture", "Three layers, three contracts. Quality and business value increase at every step.", eyebrow="Step 1 · Concept")
    .facts([
        {"title": "Bronze: keep everything", "accent": "amber", "rows": [
            ("Contract", "Exactly what the source sent, plus where and when it arrived"),
            ("Why", "Replay history, audit, fix a bug without asking the source again"),
            ("Falak", "<code>bronze.product_events</code> keeps the duplicate events")]},
        {"title": "Silver: clean and conform", "accent": "blue", "rows": [
            ("Contract", "One trustworthy, typed, deduplicated version of each entity"),
            ("Why", "Every team starts from the same clean customers, invoices, events"),
            ("Falak", "<code>silver.customers</code>: no test accounts, one country spelling")]},
        {"title": "Gold: ready for the business", "accent": "green", "rows": [
            ("Contract", "Facts and aggregates shaped for a question or a product"),
            ("Why", "Fast, simple to query for people, Genie and apps"),
            ("Falak", "<code>gold.customer_360</code>: one row per customer with a risk level")]},
    ]))

nb.slide(Slide()
    .header("Lakeflow Spark Declarative Pipelines", "You declare the tables you want. The pipeline works out the order, the compute and the incremental updates.", eyebrow="Step 1 · Concept")
    .cards([
        {"label": "Bronze", "title": "Streaming table", "accent": "amber",
         "text": "<code>CREATE OR REFRESH STREAMING TABLE ... FROM STREAM read_files(...)</code>. Reads only the new files on each update (Auto Loader)."},
        {"label": "Silver and gold", "title": "Materialized view", "accent": "blue",
         "text": "<code>CREATE OR REFRESH MATERIALIZED VIEW ... AS SELECT ...</code>. The result of a query, kept up to date by the pipeline."},
        {"label": "Quality", "title": "Expectations", "accent": "green",
         "text": "<code>CONSTRAINT valid_id EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW</code>. Tracked on every update."},
    ], kind="labeled")
    .do_dont(["One SQL file per layer: <code>01_bronze.sql</code>, <code>02_silver.sql</code>, <code>03_gold.sql</code>",
              "Refer to tables as <code>bronze.x</code>, <code>silver.x</code>, <code>gold.x</code> inside the pipeline",
              "Run the pipeline after each layer and look at the graph"],
             ["Clean data in bronze", "Hard-code row counts or dates you saw today", "Skip the data quality tab: it is where the traps show up"]))

nb.slide(Slide()
    .header("Set up Genie Code (1 minute, once)", "Genie Code is the AI assistant built into Databricks. It writes, runs and fixes code for you.", eyebrow="Step 1.0")
    .steps([
        {"title": "Open Genie Code", "text": "Click the <strong>sparkle icon</strong> at the top right of most pages."},
        {"title": "Give it the project context", "text": "<strong>More</strong> menu → <strong>Customizations</strong> → <strong>Instructions</strong> → paste the block below and save."},
        {"title": "Done", "text": "Every prompt in this guide now knows Falak, the folder layout and the naming rules."},
    ])
    .copy_prompt(GENIE_CODE_INSTRUCTIONS, label="Genie Code instructions"))

nb.slide(Slide()
    .header("Create the pipeline (2 minutes)", "One pipeline builds all three layers", eyebrow="Step 1.1")
    .steps([
        {"title": "New → ETL pipeline", "text": "Opens the Lakeflow Pipelines Editor."},
        {"title": "Settings", "items": ["Name: <code>falak_pipeline</code>", "Default catalog: <code>workspace</code>, default schema: <code>bronze</code>", "Language: <strong>SQL</strong>, start from an <strong>empty file</strong>"]},
        {"title": "Open Genie Code from inside the editor", "text": "So it creates and edits the pipeline files directly. Paste the prompts below one at a time, and click <strong>Run pipeline</strong> after each."},
    ]))

nb.slide(Slide()
    .header("Bronze: ingest everything, as delivered", "7 streaming tables, one per source folder", eyebrow="Step 1.2")
    .copy_prompt(PROMPT_BRONZE, label="Prompt: bronze"))
nb.md("**Check:** run the pipeline. You should see 7 tables in the graph, `product_events` around 1M rows. Then run this cell.")
nb.sql("""SELECT 'crm_customers' AS table_name, count(*) AS row_count FROM workspace.bronze.crm_customers
UNION ALL SELECT 'subscription_events', count(*) FROM workspace.bronze.subscription_events
UNION ALL SELECT 'invoices', count(*) FROM workspace.bronze.invoices
UNION ALL SELECT 'product_events', count(*) FROM workspace.bronze.product_events
UNION ALL SELECT 'support_tickets', count(*) FROM workspace.bronze.support_tickets
UNION ALL SELECT 'marketing_spend', count(*) FROM workspace.bronze.marketing_spend
UNION ALL SELECT 'fx_rates', count(*) FROM workspace.bronze.fx_rates""")

nb.slide(Slide(notes="""### Spoiler: what is wrong with the data

| Table | Problem |
|---|---|
| crm_customers | duplicated customers (keep the latest `last_modified`), 12 QA test accounts (`TEST ACCOUNT ...`, `@falak.io`), country spelled 5 ways, 3 date formats in `signup_date`, trailing spaces, missing industry |
| subscription_events | nested `plan` struct, MRR in AED, SAR or USD, test accounts with MRR 0 |
| invoices | `status` in mixed case, `amount` sometimes a string, three currencies |
| product_events | ~1% duplicate `event_id`, two timestamp formats, nested `context` and `properties` |
| support_tickets | English and Arabic free text, inconsistent `status`, `agent_category` filled 40% of the time |
| marketing_spend | channel codes (`paid_social`) differ from CRM labels (`Paid Social`) |
| fx_rates | `month` looks like `2024-01` but is inferred as a DATE |
""")
    .header("Play detective before cleaning (optional, 3 minutes)", "The best data engineers look before they clean. Compare with the spoiler in the notes below.", eyebrow="Step 1.3")
    .copy_prompt(PROMPT_DETECTIVE, label="Prompt: data quality detective"))

nb.slide(Slide()
    .header("Silver: clean, type, deduplicate", "7 materialized views with data quality expectations", eyebrow="Step 1.4")
    .copy_prompt(PROMPT_SILVER, label="Prompt: silver"))
nb.md("**Check:** run the pipeline, open each silver table in the graph and look at its **data quality** tab. Then run this cell: about 3,970 customers (from ~4,100 CRM rows), 6 countries, about 1.02M events (from ~1.03M), and 0 events missing an FX rate.")
nb.sql("""SELECT
  (SELECT count(*) FROM workspace.bronze.crm_customers) AS crm_rows,
  (SELECT count(*) FROM workspace.silver.customers) AS customers,
  (SELECT count(DISTINCT country) FROM workspace.silver.customers) AS countries,
  (SELECT count(*) FROM workspace.bronze.product_events) AS raw_events,
  (SELECT count(*) FROM workspace.silver.product_events) AS events,
  (SELECT count_if(mrr_aed IS NULL) FROM workspace.silver.subscription_events) AS events_missing_fx""")

nb.slide(Slide()
    .header("Gold: the tables your app and Genie use", "4 materialized views. Keep the names and columns: the starter app examples read them.", eyebrow="Step 1.5")
    .copy_prompt(PROMPT_GOLD, label="Prompt: gold"))
nb.md("**Check:** run the pipeline (4 gold tables appear), then run the two cells below.")
nb.sql("""-- October 2026 should be close to 2.0M AED and ~2,700 active customers
SELECT month, round(sum(mrr_aed)) AS mrr_aed, count_if(is_active) AS active_customers
FROM workspace.gold.mrr_monthly GROUP BY month ORDER BY month DESC LIMIT 6""")
nb.sql("""-- Rimal Logistics Co. should be at the top
SELECT company_name, country, plan_name, mrr_aed, risk_reasons
FROM workspace.gold.customer_360 WHERE status = 'active' AND risk_level = 'high'
ORDER BY mrr_aed DESC LIMIT 10""")

nb.slide(Slide()
    .header("Stretch goals for step 1", "If you are ahead, pick one", eyebrow="Step 1.6")
    .cards([
        {"title": "AI Functions", "accent": "coral", "text": "Ask Genie Code to replace the rule-based ticket topic with <code>ai_classify(description, ARRAY(...))</code>, or add <code>ai_analyze_sentiment</code>."},
        {"title": "Incremental", "accent": "blue", "text": "Run <code>02_New_Data_Drop</code>, refresh the pipeline, and check how many rows each streaming table processed."},
        {"title": "AUTO CDC", "accent": "green", "text": "Rebuild <code>silver.customers</code> with <code>AUTO CDC INTO ... KEYS (customer_id) SEQUENCE BY last_modified</code>."},
    ])
    .callout(eyebrow="Behind at minute 25?", kind="caution", icon="!", text="Stop your pipeline and run <code>99_Catch_Up</code>. Same gold tables in about 3 minutes."))

# ---- 3. metric views
nb.slide(Slide()
    .header("Metric views: define each KPI once", "Ask three people for the churn rate and you get three numbers. A metric view ends that.", eyebrow="Step 2 · Concept")
    .cards([
        {"label": "Measures", "title": "The formulas", "accent": "green", "text": "MRR, churn rate, CAC, return on spend. Written once, in YAML, governed in Unity Catalog."},
        {"label": "Dimensions", "title": "The ways to slice", "accent": "blue", "text": "Month, country, channel, plan. Any measure works with any dimension, no SQL rewrite."},
        {"label": "Consumers", "title": "Everyone agrees", "accent": "coral", "text": "Genie, AI/BI dashboards, your app and SQL all use <code>MEASURE(`MRR`)</code> and get the same number."},
    ], kind="labeled")
    .callout(eyebrow="How", kind="info", text="Open a <strong>SQL editor</strong> tab, open Genie Code there and paste the prompts below."))

nb.slide(Slide()
    .header("Revenue metrics", "On gold.mrr_monthly", eyebrow="Step 2.1")
    .copy_prompt(PROMPT_MV_REVENUE, label="Prompt: revenue metric view"))
nb.md("**Check:** October 2026 should show about 2.0M AED of MRR, and churn should spike in August.")
nb.sql("""SELECT `Month`, MEASURE(`MRR`) AS mrr_aed, MEASURE(`Active Customers`) AS active_customers,
       MEASURE(`Logo Churn Rate`) AS churn_rate, MEASURE(`Net Revenue Retention`) AS nrr
FROM workspace.gold.revenue_metrics
WHERE `Month` >= '2026-01-01'
GROUP BY ALL ORDER BY `Month`""")

nb.slide(Slide()
    .header("Acquisition metrics", "On gold.acquisition_monthly. This one tells Falak's whole marketing story.", eyebrow="Step 2.2")
    .copy_prompt(PROMPT_MV_ACQ, label="Prompt: acquisition metric view"))
nb.md("**Check:** Paid Social has the biggest spend and the cheapest leads, but one of the lowest returns on spend.")
nb.sql("""SELECT `Acquisition Channel`, MEASURE(`Marketing Spend`) AS spend_aed, MEASURE(`Cost per Lead`) AS cost_per_lead,
       MEASURE(`CAC`) AS cac, MEASURE(`Churned Share`) AS churned_share, MEASURE(`Return on Spend`) AS return_on_spend
FROM workspace.gold.acquisition_metrics
GROUP BY ALL ORDER BY spend_aed DESC""")

# ---- 4. genie
nb.slide(Slide()
    .header("Build your Genie Agent", "A natural-language analyst over the gold layer, that the founders would actually trust", eyebrow="Step 3")
    .steps([
        {"title": "New → Genie Agent", "text": "Called Genie space in older screens. Name it <code>Falak Business Analyst</code>."},
        {"title": "Add 4 data sources", "items": ["<code>workspace.gold.revenue_metrics</code> (metric view)", "<code>workspace.gold.acquisition_metrics</code> (metric view)",
                                                  "<code>workspace.gold.customer_360</code>", "<code>workspace.gold.support_tickets</code>"]},
        {"title": "Warehouse", "text": "The default <strong>Serverless Starter Warehouse</strong>."},
        {"title": "Paste the description, instructions and sample questions below", "text": "In <strong>Settings</strong> (description) and <strong>Instructions</strong> (text instructions, sample questions)."},
    ]))

nb.slide(Slide()
    .header("Teach it the business", "Copy each block into the matching field: description in Settings, the rest in Instructions", eyebrow="Step 3.1")
    .copy_prompt(GENIE_DESCRIPTION, label="Description")
    .copy_prompt(GENIE_INSTRUCTIONS, label="Instructions")
    .copy_prompt(GENIE_QUESTIONS, label="Sample questions (one per line)"))

nb.slide(Slide()
    .header("5 prompts to try", "Validated on the Falak data. Each one uncovers a story the founders did not see.", eyebrow="Step 3.2")
    .table(["#", "The story", "What Genie found in our test"], [
        ["1", "Who we might lose next", "Rimal Logistics Co. (Riyadh, Scale, ~5,000 AED MRR) at the top: usage down 60-70%, 2 failed invoices, a cancellation ticket. Then four Scale accounts with usage down 50%+"],
        ["2", "Growth at any cost", "Paid Social: 7.6M AED spent, ~5,400 AED CAC, return on spend only ~1.1-1.2x, below the 1.3 threshold"],
        ["3", "The KSA incident", "MRR grew until July, then in August churn jumped to 80 customers, net new MRR turned negative, and payment-failure tickets dominated support (344 over the summer)"],
        ["4", "The activation lever", "~14% churn for customers who connected an integration in their first 14 days vs ~43% for the rest: 3x less"],
        ["5", "A product opportunity", "e-invoicing is the #1 UAE support topic since March 2026 (~500 tickets), ahead of how-to and billing questions"],
    ])
    .copy_prompt("Who are our 5 biggest at-risk accounts, and why are they at risk?", label="Prompt 1 · Who we might lose next")
    .copy_prompt("Where are we wasting the most marketing money?", label="Prompt 2 · Growth at any cost")
    .copy_prompt("What happened in Saudi Arabia in summer 2026?", label="Prompt 3 · The KSA incident")
    .copy_prompt("Do customers who connect an integration in their first 14 days churn less? Compare the churn rate of both groups.", label="Prompt 4 · The activation lever")
    .copy_prompt("What are UAE customers asking support about since March 2026, and what does it tell us about the product?", label="Prompt 5 · A product opportunity"))

nb.md("""**Answer not right?** Improve the instructions, or add an example SQL query in **Instructions → SQL queries**, then ask again. Without the last instruction line ("investigate like an analyst"), prompt 3 only looks at MRR and misses the incident: a good example of how much instructions matter.""")

nb.slide(Slide()
    .header("Plug it into your app", "Copy the Genie Agent ID: open the agent → About, or take it from the URL <code>.../genie/rooms/&lt;ID&gt;</code>", eyebrow="Step 3.3")
    .callout(eyebrow="Then, in Claude Code", kind="success",
             title="Open guides/4_App_with_Claude.md on your laptop",
             text="Tell Claude: <em>\"Connect to my app (profile hackathon). Add the Overview page from examples, connect my Genie Agent &lt;ID&gt; and add the Ask Genie page. Deploy.\"</em> "
                  "Then spend the rest of the time on your own idea.")
    .band("Demo: the problem in one sentence, one live Genie question, one app feature, what you would build next week.", accent="coral"))

nb.write(OUT)
print("wrote", OUT)
