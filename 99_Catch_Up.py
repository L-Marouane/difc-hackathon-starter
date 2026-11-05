# Databricks notebook source
# MAGIC %md
# MAGIC # 99 · Catch-up: build the reference gold layer in one click
# MAGIC
# MAGIC Behind schedule, or want to go straight to Genie and the app? Run all cells.
# MAGIC It creates the pipeline `falak_reference_pipeline` from `reference/pipeline/` (bronze, silver, gold),
# MAGIC runs it, then creates the two metric views. About 5 minutes.
# MAGIC
# MAGIC Prerequisite: `00_Setup_Data` has run.
# MAGIC
# MAGIC Free Edition allows one active pipeline per type: if your own pipeline is running, stop it first.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace", "Catalog")
CATALOG = dbutils.widgets.get("catalog")

# COMMAND ----------

import os
import time

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
api = w.api_client.do  # raw REST: works whatever SDK version the serverless environment ships
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = os.path.dirname(notebook_path)
files = [f"{repo_root}/reference/pipeline/{f}" for f in ["01_bronze.sql", "02_silver.sql", "03_gold.sql"]]

# The reference SQL targets Free Edition's `workspace` catalog. For another catalog, write adjusted copies.
if CATALOG != "workspace":
    import base64
    copies = f"{repo_root}/reference/pipeline_{CATALOG}"
    w.workspace.mkdirs(copies)
    for i, p in enumerate(files):
        with open(f"/Workspace{p}") as f:
            sql = f.read().replace("/Volumes/workspace/", f"/Volumes/{CATALOG}/")
        files[i] = f"{copies}/{os.path.basename(p)}"
        api("POST", "/api/2.0/workspace/import", body={"path": files[i], "format": "RAW", "overwrite": True,
                                                     "content": base64.b64encode(sql.encode()).decode()})
print("\n".join(files))

# COMMAND ----------

NAME = "falak_reference_pipeline"
spec = {
    "name": NAME,
    "catalog": CATALOG,
    "schema": "bronze",
    "serverless": True,
    "channel": "CURRENT",
    "development": True,
    "libraries": [{"file": {"path": p}} for p in files],
}
existing = api("GET", "/api/2.0/pipelines", query={"filter": f"name LIKE '{NAME}'"}).get("statuses", [])
if existing:
    pipeline_id = existing[0]["pipeline_id"]
    api("PUT", f"/api/2.0/pipelines/{pipeline_id}", body={**spec, "id": pipeline_id})
else:
    pipeline_id = api("POST", "/api/2.0/pipelines", body=spec)["pipeline_id"]
print(f"Pipeline: {w.config.host}/pipelines/{pipeline_id}")

update_id = api("POST", f"/api/2.0/pipelines/{pipeline_id}/updates", body={"full_refresh": True})["update_id"]
while True:
    state = api("GET", f"/api/2.0/pipelines/{pipeline_id}/updates/{update_id}")["update"]["state"]
    print(time.strftime("%H:%M:%S"), state)
    if state in ("COMPLETED", "FAILED", "CANCELED"):
        break
    time.sleep(20)
assert state == "COMPLETED", "Pipeline failed: open the pipeline link above to see the error."

# COMMAND ----------

with open(f"/Workspace{repo_root}/reference/metric_views.sql") as f:
    sql_text = f.read().replace("workspace.gold.", f"{CATALOG}.gold.")
for stmt in [s.strip() + "$$" for s in sql_text.split("$$;") if "CREATE" in s]:
    stmt = stmt[stmt.index("CREATE"):]
    spark.sql(stmt)
    print("created", stmt.split("\n")[0])

# COMMAND ----------

display(spark.sql(f"""
  SELECT `Month`, MEASURE(`MRR`) AS mrr_aed, MEASURE(`Active Customers`) AS active_customers,
         MEASURE(`Logo Churn Rate`) AS logo_churn_rate
  FROM {CATALOG}.gold.revenue_metrics
  WHERE `Month` >= '2026-01-01'
  GROUP BY ALL ORDER BY `Month`"""))

# COMMAND ----------

# MAGIC %md
# MAGIC Done. Continue with **`01_Hackathon_Guide`**, step 3 (Genie Agent).
