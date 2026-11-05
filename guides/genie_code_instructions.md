Project: Falak, a fictional Dubai startup selling invoicing and payment-link software to SMEs in the GCC (UAE, KSA, Qatar, Bahrain, Oman, Kuwait). Plans: Starter, Growth, Scale. Currencies AED, SAR, USD. Report money in AED.

Data layout (Unity Catalog, catalog `workspace`):
- Raw files: /Volumes/workspace/raw/landing/ with folders crm/, billing/subscription_events/, billing/invoices/, product_events/, support/tickets/, marketing/, reference/
- Schemas: bronze (raw as-is), silver (clean), gold (business tables)
- Gold contract used by the app: gold.mrr_monthly, gold.customer_360, gold.acquisition_monthly, gold.support_tickets

Rules:
- Pipelines are Lakeflow Spark Declarative Pipelines in SQL. Bronze = STREAMING TABLE with STREAM read_files on a folder. Silver and gold = MATERIALIZED VIEW.
- Always use two-part names in pipeline code (bronze.x, silver.x, gold.x) and three-part names elsewhere (workspace.gold.x).
- One SQL file per layer: 01_bronze.sql, 02_silver.sql, 03_gold.sql.
- Add a COMMENT to every table. Use expectations (CONSTRAINT ... EXPECT) for data quality in silver.
- Use serverless compute. Keep queries simple and readable, this code will be shown on stage.
