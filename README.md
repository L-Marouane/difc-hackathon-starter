# DIFC Startup Hackathon · Databricks starter kit

In about an hour you will take a startup's messy raw data and ship an AI-powered app on top of it:

```
raw files ──► pipeline (bronze → silver → gold) ──► metric views ──► Genie Agent ──► your app
  Step 0         Step 1 · Genie Code                 Step 2           Step 3          Step 4 · Claude Code
```

## The startup: Falak

Falak is a fictional Dubai startup selling invoicing and payment links to SMEs across the GCC.
It has 2,700 paying customers, 2.0M AED of MRR, six source systems, and some problems hiding in the data.
**Your job is to find the problems and build the tool the founders need to act on them.**

## Before you arrive (20 minutes)

**Everyone**

1. Create a [Databricks Free Edition](https://www.databricks.com/learn/free-edition) account and log in once.
2. Download this repo: **Code** → **Download ZIP**, and unzip it on your laptop.

**To build the app with Claude Code (step 4)**

| Tool | Why | Install | Check |
|---|---|---|---|
| Node.js 22+ | The app is TypeScript + React | [nodejs.org](https://nodejs.org/en/download) (LTS) | `node --version` |
| Databricks CLI 1.17+ | Claude deploys the app and queries your data with it | [docs.databricks.com/dev-tools/cli/install](https://docs.databricks.com/aws/en/dev-tools/cli/install) | `databricks --version` |
| Claude Code | Your AI pair programmer in the terminal | [docs.claude.com/claude-code](https://docs.claude.com/en/docs/claude-code/overview) | `claude --version` |
| Databricks AI Dev Kit | Gives Claude Databricks skills and an MCP server (tables, SQL, Genie, apps) | [github.com/databricks-solutions/ai-dev-kit](https://github.com/databricks-solutions/ai-dev-kit), see below | `/mcp` inside Claude |

Then:

```bash
# 1. Log the CLI in to your Free Edition workspace (opens the browser)
databricks auth login --host https://<your-workspace>.cloud.databricks.com --profile hackathon

# 2. Install the AI Dev Kit: skills + MCP server for Claude Code (answer the prompts, pick the "hackathon" profile)
bash <(curl -sL https://raw.githubusercontent.com/databricks-solutions/ai-dev-kit/main/install.sh)
#    Windows (PowerShell): irm https://raw.githubusercontent.com/databricks-solutions/ai-dev-kit/main/install.ps1 | iex

# 3. Check: start Claude in the app folder, type /mcp and you should see the Databricks server
cd difc-hackathon-starter/app && npm install && claude
```

## Step 0 · Get the kit into your workspace (5 minutes)

1. In Databricks: **Workspace** → **Create** → **Git folder** → paste this repo URL.
2. Open **`00_Setup_Data`**, click **Run all** (about 5 minutes), then open **`01_Hackathon_Guide`** while it runs. It lands about 1M rows of raw data in `/Volumes/workspace/raw/landing/` and deploys your starter app, `falak-app`.

## The steps

| Step | Guide | Tool | Time |
|---|---|---|---|
| 1 | Pipeline: bronze, silver, gold (`01_Hackathon_Guide`, step 1) | Genie Code in the Lakeflow Pipelines Editor | 25 min |
| 2 | Metric views (`01_Hackathon_Guide`, step 2) | Genie Code in the SQL editor | 10 min |
| 3 | Genie Agent (`01_Hackathon_Guide`, step 3) | Genie | 10 min |
| 4 | [App](guides/4_App_with_Claude.md) | Claude Code on your laptop | 25 min |

**Behind schedule?** Run **`99_Catch_Up`**: it builds the reference pipeline and metric views in about 5 minutes, then go to Step 3.
**Ahead?** Each guide ends with stretch goals, and `02_New_Data_Drop` simulates new data arriving.

## What is in the box

| Path | What |
|---|---|
| `00_Setup_Data`, `02_New_Data_Drop`, `_generator` | Data generation + starter app deployment (run on serverless) |
| `01_Hackathon_Guide` | The guide: context, then steps 1-3 with copy-paste Genie Code prompts and check cells |
| `guides/` | Step 4 (app with Claude Code) and the Genie Code instructions block |
| `reference/` | Reference pipeline and metric views (the answer key) |
| `99_Catch_Up` | One-click reference build |
| `app/` | Starter AppKit app (TypeScript + React) deployed by `00_Setup_Data`, plus tested example pages, ready for Claude Code |

## Judging

1. **Insight:** did you find a real problem in the data and quantify it?
2. **Product:** would a founder use your app on Monday morning?
3. **Craft:** clean pipeline, governed metrics, Genie answers that are right.
