-- BRONZE: ingest every source as-is with Auto Loader (incremental: only new files are read on each update).
-- Pipeline settings: default catalog = workspace, default schema = bronze (99_Catch_Up sets this for you).

CREATE OR REFRESH STREAMING TABLE bronze.crm_customers
COMMENT "CRM exports as delivered. Contains duplicates, QA test accounts and mixed date formats."
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/workspace/raw/landing/crm/', format => 'csv', header => true);

CREATE OR REFRESH STREAMING TABLE bronze.subscription_events
COMMENT "Billing system subscription lifecycle events (new, upgrade, downgrade, seat_change, churn, reactivation)."
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/workspace/raw/landing/billing/subscription_events/', format => 'json');

CREATE OR REFRESH STREAMING TABLE bronze.invoices
COMMENT "Billing system invoices. Status casing and amount type are inconsistent."
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/workspace/raw/landing/billing/invoices/', format => 'json',
                       schemaHints => 'amount STRING');

CREATE OR REFRESH STREAMING TABLE bronze.product_events
COMMENT "Product analytics events from web and mobile apps. About 1% duplicates from client retries."
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/workspace/raw/landing/product_events/', format => 'json');

CREATE OR REFRESH STREAMING TABLE bronze.support_tickets
COMMENT "Support desk tickets with free-text subject and description, English and Arabic."
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/workspace/raw/landing/support/tickets/', format => 'json');

CREATE OR REFRESH STREAMING TABLE bronze.marketing_spend
COMMENT "Monthly marketing spend by channel code."
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/workspace/raw/landing/marketing/', format => 'csv', header => true);

CREATE OR REFRESH STREAMING TABLE bronze.fx_rates
COMMENT "Monthly FX rates to AED."
AS SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/workspace/raw/landing/reference/', format => 'csv', header => true);
