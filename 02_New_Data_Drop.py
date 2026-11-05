# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · New data drop (optional)
# MAGIC
# MAGIC Simulates four more days of Falak (1 to 4 November 2026) landing in the volume:
# MAGIC new signups, a CRM delta export, new invoices and tickets, fresh product events,
# MAGIC and a handful of **late-arriving October events**.
# MAGIC
# MAGIC Run it after your pipeline works, then refresh the pipeline. Streaming tables should only process the new files.

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace", "Catalog")
CATALOG = dbutils.widgets.get("catalog")
LANDING = f"/Volumes/{CATALOG}/raw/landing"

# COMMAND ----------

# MAGIC %run ./_generator

# COMMAND ----------

import shutil

LOCAL = "/tmp/falak_landing_drop"
shutil.rmtree(LOCAL, ignore_errors=True)

world = build_world()  # same seed as 00_Setup_Data, so the drop continues the same story
stats = write_batch(world, LOCAL, batch=2)
shutil.copytree(LOCAL, LANDING, dirs_exist_ok=True)

for k, v in stats.items():
    print(f"{k:30s} {v:>10,} new rows")
print("\nNow refresh your pipeline.")
