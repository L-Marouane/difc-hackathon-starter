# Examples: tested pages to drop into the app

These pages were built and tested on the Falak gold contract. They are not compiled until you copy them in.

## Overview page (KPIs, MRR trend, MRR gained vs lost, at-risk accounts)

Needs `workspace.gold.mrr_monthly` and `workspace.gold.customer_360`.

1. Copy `examples/overview/queries/*.sql` to `config/queries/`
2. Copy `examples/overview/OverviewPage.tsx` to `client/src/pages/overview/`
3. Add a route `/overview` and a NavLink in `client/src/App.tsx` (or make it the home route)
4. `npm run typegen`, then `npm run deploy:app`

If the founder's gold tables differ from the contract, adapt the SQL first (`databricks experimental aitools tools discover-schema ...`).

## Ask Genie page

Needs the founder's Genie Agent ID.

1. `node scripts/connect-genie.mjs --space <genie-agent-id>` (attaches the agent to the app, updates `app.yaml` and `.env`)
2. In `server/server.ts`: `import { createApp, analytics, genie, server } from '@databricks/appkit'` and add `genie()` to `plugins`
3. Copy `examples/genie/GeniePage.tsx` to `client/src/pages/genie/`, add a `/genie` route and a NavLink
4. `npm run deploy:app`
