-- Reference metric views. Run in the SQL editor (or a notebook cell with %sql) after the pipeline has built gold.

CREATE OR REPLACE VIEW workspace.gold.revenue_metrics
WITH METRICS
LANGUAGE YAML
AS $$
version: 1.1
source: workspace.gold.mrr_monthly
comment: "Falak subscription revenue metrics. One source row per customer per month. MRR is a monthly snapshot, so always slice MRR by Month."
dimensions:
  - name: Month
    expr: month
    comment: "Calendar month (first day of month)"
  - name: Country
    expr: country
  - name: Industry
    expr: industry
  - name: Company Size
    expr: company_size
  - name: Acquisition Channel
    expr: acquisition_channel
    synonyms: ["channel", "marketing channel", "source"]
  - name: Plan
    expr: plan_name
  - name: Signup Cohort
    expr: signup_cohort
    comment: "Month the customer signed up"
  - name: Movement
    expr: movement
    comment: "new, expansion, contraction, churn, reactivation or flat"
measures:
  - name: MRR
    expr: SUM(mrr_aed)
    comment: "Monthly recurring revenue in AED. Only meaningful per month."
    synonyms: ["monthly recurring revenue", "revenue", "MRR AED"]
  - name: Active Customers
    expr: COUNT(DISTINCT CASE WHEN is_active THEN customer_id END)
    synonyms: ["paying customers", "customers", "logos"]
  - name: ARPA
    expr: SUM(mrr_aed) / NULLIF(COUNT(DISTINCT CASE WHEN is_active THEN customer_id END), 0)
    comment: "Average revenue per active account in AED"
    synonyms: ["average revenue per account"]
  - name: New MRR
    expr: SUM(new_mrr_aed)
  - name: Expansion MRR
    expr: SUM(expansion_mrr_aed)
  - name: Contraction MRR
    expr: SUM(contraction_mrr_aed)
  - name: Churned MRR
    expr: SUM(churned_mrr_aed)
    synonyms: ["lost MRR", "churn MRR"]
  - name: Reactivation MRR
    expr: SUM(reactivation_mrr_aed)
  - name: Net New MRR
    expr: SUM(new_mrr_aed + expansion_mrr_aed + reactivation_mrr_aed - contraction_mrr_aed - churned_mrr_aed)
  - name: Churned Customers
    expr: COUNT(DISTINCT CASE WHEN movement = 'churn' THEN customer_id END)
    synonyms: ["lost customers", "churned logos"]
  - name: Logo Churn Rate
    expr: COUNT(DISTINCT CASE WHEN movement = 'churn' THEN customer_id END) / NULLIF(COUNT(DISTINCT CASE WHEN prev_mrr_aed > 0 THEN customer_id END), 0)
    comment: "Customers lost in the month divided by customers paying at the start of the month"
    synonyms: ["churn rate", "customer churn rate"]
  - name: Net Revenue Retention
    expr: SUM(CASE WHEN prev_mrr_aed > 0 THEN mrr_aed ELSE 0 END) / NULLIF(SUM(prev_mrr_aed), 0)
    comment: "Monthly NRR: this month's MRR from customers who were paying last month, divided by their MRR last month"
    synonyms: ["NRR", "net dollar retention"]
$$;

CREATE OR REPLACE VIEW workspace.gold.acquisition_metrics
WITH METRICS
LANGUAGE YAML
AS $$
version: 1.1
source: workspace.gold.acquisition_monthly
comment: "Falak acquisition economics by channel and signup month. Revenue to date is what each signup cohort has paid so far."
dimensions:
  - name: Month
    expr: month
  - name: Acquisition Channel
    expr: acquisition_channel
    synonyms: ["channel", "marketing channel", "source"]
measures:
  - name: Marketing Spend
    expr: SUM(spend_aed)
    comment: "AED"
    synonyms: ["spend", "marketing cost", "ad spend"]
  - name: Leads
    expr: SUM(leads)
  - name: Signups
    expr: SUM(signups)
    synonyms: ["new customers", "acquired customers"]
  - name: CAC
    expr: SUM(spend_aed) / NULLIF(SUM(signups), 0)
    comment: "Customer acquisition cost in AED: spend divided by signups"
    synonyms: ["customer acquisition cost", "cost per customer"]
  - name: Cost per Lead
    expr: SUM(spend_aed) / NULLIF(SUM(leads), 0)
    synonyms: ["CPL"]
  - name: Activation Rate
    expr: SUM(activated_signups) / NULLIF(SUM(signups), 0)
    comment: "Share of signups that connected an integration within 14 days"
  - name: Churned Share
    expr: SUM(churned_to_date) / NULLIF(SUM(signups), 0)
    comment: "Share of signups that have churned by today"
  - name: Revenue to Date
    expr: SUM(revenue_to_date_aed)
  - name: Return on Spend
    expr: SUM(revenue_to_date_aed) / NULLIF(SUM(spend_aed), 0)
    comment: "Revenue collected to date divided by marketing spend. Above 1 means the channel has paid back."
    synonyms: ["ROAS", "payback", "LTV to CAC", "return on marketing spend"]
$$;
