# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Setup: Falak's raw data + your starter app
# MAGIC
# MAGIC **Falak** is a fictional Dubai startup: invoicing and payment links for SMEs across the GCC.
# MAGIC 2,700 paying customers, 2.0M AED of MRR, six source systems, and a few problems hiding in the data.
# MAGIC
# MAGIC This notebook:
# MAGIC 1. creates your schemas and drops Falak's raw exports into a Unity Catalog volume, exactly as the source systems would deliver them
# MAGIC 2. deploys **`falak-app`**, an almost empty Databricks App already wired to your lakehouse, ready for Claude Code
# MAGIC
# MAGIC **Run all cells (about 6 minutes on serverless).**
# MAGIC
# MAGIC | Source system | Folder in the volume | Format | Rows |
# MAGIC |---|---|---|---|
# MAGIC | CRM (HubSpot-style export) | `crm/` | CSV | ~4.1k |
# MAGIC | Billing: subscription events | `billing/subscription_events/` | JSON lines, nested `plan` | ~8.5k |
# MAGIC | Billing: invoices | `billing/invoices/` | JSON lines | ~34k |
# MAGIC | Product analytics events | `product_events/` | JSON lines, nested `context` | ~1.0M |
# MAGIC | Support desk tickets | `support/tickets/` | JSON lines, English + Arabic free text | ~5.3k |
# MAGIC | Marketing spend | `marketing/` | CSV | 204 |
# MAGIC | FX rates | `reference/` | CSV | 105 |
# MAGIC
# MAGIC The data is deliberately messy (duplicates, test accounts, mixed date formats, three currencies,
# MAGIC inconsistent status values). Cleaning it is your job in the pipeline step.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace", "Catalog")
dbutils.widgets.dropdown("deploy_app", "yes", ["yes", "no"], "Deploy the starter app")
dbutils.widgets.dropdown("reset_app", "no", ["no", "yes"], "Reset the app to the starter version")
CATALOG = dbutils.widgets.get("catalog")
LANDING = f"/Volumes/{CATALOG}/raw/landing"
APP_NAME = "falak-app"
DEPLOY_APP = dbutils.widgets.get("deploy_app") == "yes"
RESET_APP = dbutils.widgets.get("reset_app") == "yes"

# COMMAND ----------

# MAGIC %run ./_generator

# COMMAND ----------

for schema in ["raw", "bronze", "silver", "gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{schema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.raw.landing COMMENT 'Raw exports from Falak source systems'")
spark.sql(f"COMMENT ON SCHEMA {CATALOG}.raw IS 'Landing zone: raw files from source systems'")
spark.sql(f"COMMENT ON SCHEMA {CATALOG}.bronze IS 'Raw data ingested as-is, one table per source'")
spark.sql(f"COMMENT ON SCHEMA {CATALOG}.silver IS 'Cleaned, deduplicated, typed data'")
spark.sql(f"COMMENT ON SCHEMA {CATALOG}.gold IS 'Business-ready tables for Genie, metric views and the app'")
print("Schemas and volume ready:", LANDING)

# COMMAND ----------

# Create the app now so its compute starts while the data is generated
import base64
import os
import time

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
api = w.api_client.do  # raw REST: works whatever SDK version the serverless environment ships

app_exists = False
if DEPLOY_APP:
    try:
        api("GET", f"/api/2.0/apps/{APP_NAME}")
        app_exists = True
        print(f"App {APP_NAME} already exists")
    except Exception:
        api("POST", "/api/2.0/apps", body={"name": APP_NAME, "description": "Falak Founder Console (DIFC hackathon starter)"})
        print(f"Creating app {APP_NAME}: compute is starting in the background")

# COMMAND ----------

import shutil

LOCAL = "/tmp/falak_landing"
shutil.rmtree(LOCAL, ignore_errors=True)

world = build_world()
stats = write_batch(world, LOCAL, batch=1)

# start from a clean landing zone so re-running never duplicates files
for sub in ["crm", "billing", "product_events", "support", "marketing", "reference"]:
    dbutils.fs.rm(f"{LANDING}/{sub}", recurse=True)
shutil.copytree(LOCAL, LANDING, dirs_exist_ok=True)

for k, v in stats.items():
    print(f"{k:30s} {v:>10,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Peek at the raw files
# MAGIC Notice the nested `plan` struct, the `country` spelled five ways, and `amount` that is sometimes a string.

# COMMAND ----------

display(spark.sql(f"SELECT * FROM read_files('{LANDING}/billing/invoices/', format => 'json') LIMIT 10"))

# COMMAND ----------

display(spark.sql(f"""
  SELECT country, count(*) AS rows
  FROM read_files('{LANDING}/crm/', format => 'csv', header => true)
  GROUP BY country ORDER BY rows DESC"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Deploy the starter app
# MAGIC Copies `app/` from this folder into your workspace, attaches the SQL warehouse, gives the app read access
# MAGIC to bronze, silver and gold, and deploys it. If the app already has a deployment it is left untouched
# MAGIC (set `reset_app` = yes to go back to the starter version).

# COMMAND ----------

def wait_compute(minutes=10):
    deadline = time.time() + minutes * 60
    while time.time() < deadline:
        state = (api("GET", f"/api/2.0/apps/{APP_NAME}").get("compute_status") or {}).get("state", "")
        if state == "ACTIVE":
            return True
        if state in ("STOPPED", "ERROR"):
            api("POST", f"/api/2.0/apps/{APP_NAME}/start")
        time.sleep(10)
    return False


app_url = None
if DEPLOY_APP:
    app = api("GET", f"/api/2.0/apps/{APP_NAME}")
    if app.get("active_deployment") and not RESET_APP:
        app_url = app.get("url")
        print(f"{APP_NAME} is already deployed, leaving your version untouched: {app_url}")
    else:
        # 1. app source: <your home>/falak-app, copied from app/ in this folder
        me = w.current_user.me().user_name
        notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
        local_app = f"/Workspace{os.path.dirname(notebook_path)}/app"
        src = f"/Workspace/Users/{me}/{APP_NAME}"
        skip = {"node_modules", "dist", ".databricks", ".env"}
        n = 0
        for root, dirs, files in os.walk(local_app):
            dirs[:] = [d for d in dirs if d not in skip]
            for f in files:
                if f in skip:
                    continue
                rel = os.path.relpath(os.path.join(root, f), local_app)
                with open(os.path.join(root, f), "rb") as fh:
                    data = fh.read()
                if CATALOG != "workspace" and rel.endswith(".sql"):
                    data = data.replace(b"workspace.", f"{CATALOG}.".encode())
                w.workspace.mkdirs(os.path.dirname(f"{src}/{rel}"))
                api("POST", "/api/2.0/workspace/import", body={"path": f"{src}/{rel}", "format": "RAW", "overwrite": True,
                                                              "content": base64.b64encode(data).decode()})
                n += 1
        print(f"App source: {n} files written to {src}")

        # 2. SQL warehouse (Free Edition has one: Serverless Starter Warehouse)
        warehouses = api("GET", "/api/2.0/sql/warehouses").get("warehouses", [])
        wh = next((x for x in warehouses if "starter" in x["name"].lower()), warehouses[0])["id"]

        # 3. wait for compute, attach the warehouse, grant the app's identity read access
        assert wait_compute(), "App compute did not start in 10 minutes: rerun this cell"
        api("PATCH", f"/api/2.0/apps/{APP_NAME}", body={"name": APP_NAME, "resources": [
            {"name": "sql-warehouse", "sql_warehouse": {"id": wh, "permission": "CAN_USE"}}]})
        sp = api("GET", f"/api/2.0/apps/{APP_NAME}")["service_principal_client_id"]
        spark.sql(f"GRANT USE CATALOG ON CATALOG {CATALOG} TO `{sp}`")
        for schema in ["bronze", "silver", "gold"]:
            spark.sql(f"GRANT USE SCHEMA, SELECT ON SCHEMA {CATALOG}.{schema} TO `{sp}`")

        # 4. deploy (the build installs npm packages; retry once on a transient failure)
        for attempt in (1, 2):
            dep = api("POST", f"/api/2.0/apps/{APP_NAME}/deployments", body={"source_code_path": src, "mode": "SNAPSHOT"})
            while True:
                st = api("GET", f"/api/2.0/apps/{APP_NAME}/deployments/{dep['deployment_id']}").get("status") or {}
                if st.get("state") in ("SUCCEEDED", "FAILED", "CANCELLED"):
                    break
                time.sleep(10)
            print(f"Deployment attempt {attempt}: {st.get('state')} {(st.get('message') or '')[:200]}")
            if st.get("state") == "SUCCEEDED":
                break
        app_url = api("GET", f"/api/2.0/apps/{APP_NAME}").get("url")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Done. Next steps
# MAGIC 1. Open the app link printed below: it shows your lakehouse filling up as you build.
# MAGIC 2. Open **`01_Hackathon_Guide`** and build bronze → silver → gold with Genie Code.
# MAGIC 3. On your laptop, in the `app/` folder: `node scripts/configure.mjs --profile <your-cli-profile>`, then `claude`.
# MAGIC
# MAGIC Later in the hackathon, run **`02_New_Data_Drop`** to simulate a new day of data arriving and watch your pipeline pick it up incrementally.

# COMMAND ----------

print(f"Data:  {LANDING}")
print(f"App:   {app_url or 'not deployed (deploy_app = no)'}")
