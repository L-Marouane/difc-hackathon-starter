# Falak Founder Console: instructions for Claude

Work in small, safe steps: deploy early and never leave the app broken.

## What this app is

A Databricks App built with AppKit (Node/TypeScript backend + React frontend) for **Falak**, a fictional Dubai startup selling invoicing and payment links to SMEs across the GCC. Money is in AED.

The `00_Setup_Data` notebook already **created and deployed** this app as `falak-app` in the founder's workspace, wired to the SQL warehouse, with read access to `bronze`, `silver` and `gold`. It is deliberately almost empty: your job is to build the founder's ideas on top.

- `client/src/pages/home/HomePage.tsx`: lakehouse status (tables per layer) and next steps
- `client/src/App.tsx`: layout and routes. Add new pages here.
- `config/queries/*.sql`: one SQL file per query; the file name is the `queryKey`. Parameters: `-- @param name TYPE` + `:name`.
- `server/server.ts`: plugins (`analytics`, `server`). Add `genie()` when a Genie Agent is connected. Custom API routes go here.
- `examples/`: **tested pages ready to drop in**: an Overview page (KPIs, MRR trend, at-risk accounts) and an Ask Genie page. See `examples/README.md`.
- `scripts/configure.mjs`: connects this folder to the deployed app (writes `.env`)
- `scripts/deploy.mjs` (`npm run deploy:app`): typecheck, lint, build, grants, upload, deploy
- `scripts/connect-genie.mjs`: attaches the founder's Genie Agent to the app

## The data (Unity Catalog, catalog `workspace`, schema `gold`)

The founder built these with a pipeline. Always check the real columns before writing SQL:
`databricks experimental aitools tools discover-schema workspace.gold.<table> --profile <PROFILE>`

| Object | Grain | Key columns |
|---|---|---|
| `workspace.gold.mrr_monthly` | customer x month | month, customer_id, company_name, country, acquisition_channel, plan_name, mrr_aed, prev_mrr_aed, is_active, movement, new/expansion/contraction/churned/reactivation_mrr_aed |
| `workspace.gold.customer_360` | customer | profile, status, plan_name, mrr_aed, activated_14d, events_last_30d, usage_change_pct, failed_invoices_90d, open_tickets, risk_level, risk_reasons, account_manager, as_of_date |
| `workspace.gold.acquisition_monthly` | channel x month | spend_aed, leads, signups, activated_signups, churned_to_date, revenue_to_date_aed |
| `workspace.gold.support_tickets` | ticket | created_month, topic, subject, description, status, resolution_hours, csat_score, country |
| `workspace.gold.revenue_metrics` | metric view | query with ``MEASURE(`MRR`)``, ``MEASURE(`Logo Churn Rate`)`` grouped by dimensions |
| `workspace.gold.acquisition_metrics` | metric view | ``MEASURE(`CAC`)``, ``MEASURE(`Return on Spend`)`` |

The data is historical: "today" is `max(as_of_date)` in customer_360 (end of October 2026). Never use `current_date()`.

## First-time setup (do this first, about 1 minute)

1. Ask for the founder's CLI profile name if they did not give it. Check it: `databricks auth describe --profile <PROFILE>`.
2. `npm install` (if `node_modules` is missing).
3. `node scripts/configure.mjs --profile <PROFILE>`. It finds `falak-app`, its warehouse and its source folder, and writes `.env`. If it says the app is missing, the founder must run `00_Setup_Data` first.
4. Show the founder the app URL it printed, then ask what they want to build.

Quick wins to offer once the founder has gold tables and a Genie Agent: "add the Overview page from examples" and "connect my Genie Agent <id>" (recipes in `examples/README.md`).

If a query fails because a gold table or column does not exist, the founder's gold layer differs from the contract: inspect it with `discover-schema` and adapt the SQL, or tell them to run the `99_Catch_Up` notebook in their workspace (builds the reference gold layer in about 3 minutes).

## How to add features

- **New data on screen:** add a `.sql` file in `config/queries/`, run `npm run typegen`, then use `queryKey` in a chart (`LineChart`, `BarChart`, `AreaChart`, `PieChart`, `DataTable`) or `useAnalyticsQuery`. Always pass `parameters={{}}` even with no params. Never add an Express route for a SELECT.
- **Metric views:** prefer querying `revenue_metrics` / `acquisition_metrics` with `MEASURE()` over re-implementing a KPI.
- **Calling an LLM** (drafting emails, summaries): list chat models with `databricks serving-endpoints list --profile <PROFILE>` and pick one that exists in this workspace (Free Edition has a limited set). Call it from a server route in `server/server.ts`. Attach it to the app with `databricks api patch /api/2.0/apps/falak-app` (keep the existing `resources` and add a `serving_endpoint` with `CAN_QUERY`), and reference it in `app.yaml` with `valueFrom`. See `npx @databricks/appkit docs ./docs/plugins/model-serving.md`.
- **Component props:** check `npx @databricks/appkit docs` before using an AppKit component or API. Do not guess props (charts use `xKey`/`yKey`, not Recharts names).
- **Validate before deploying:** `npm run typecheck && npm run lint`.
- **Local preview:** `npm run dev`, then http://localhost:8000 (uses the founder's CLI profile from `.env`).
- **Deploy:** `npm run deploy:app` (about 2 minutes). It validates locally first, so fix any typecheck/lint/SQL error it reports before retrying. Check status with `databricks apps get falak-app --profile <PROFILE>`, logs with `databricks apps logs falak-app --profile <PROFILE>`.
- **Genie:** `node scripts/connect-genie.mjs --space <id>` handles the app resource and `app.yaml`; you add `genie()` to `server/server.ts` and the page from `examples/genie/`.

## Free Edition limits to respect

One SQL warehouse (2X-Small), up to 3 apps, apps stop 24 hours after their last start or deploy, restricted outbound internet (no calls to external APIs from the app), limited set of foundation models.

## Style

Keep the UI clean: one idea per page, Cards for sections, AED with thousands separators, loading skeletons and friendly error messages. Never use `as unknown as T`; parse rows with zod like `OverviewPage.tsx` does.

<!-- appkit-instructions-start -->

## Databricks AppKit

This project uses Databricks AppKit packages. For AI assistant guidance on using these packages, refer to:

- **@databricks/appkit** (Backend SDK): [./node_modules/@databricks/appkit/CLAUDE.md](./node_modules/@databricks/appkit/CLAUDE.md)
- **@databricks/appkit-ui** (UI Integration, Charts, Tables, SSE, and more.): [./node_modules/@databricks/appkit-ui/CLAUDE.md](./node_modules/@databricks/appkit-ui/CLAUDE.md)

### Databricks Skills

For enhanced AI assistance with Databricks CLI operations, authentication, data exploration, and app development, install the Databricks skills:

```bash
databricks aitools install
```

<!-- appkit-instructions-end -->
