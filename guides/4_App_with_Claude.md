# Step 4 · Ship an app with Claude Code

**Goal:** turn the starter app into the tool Falak's founders need, with Claude Code.
**Time box:** 25 minutes. Connecting takes 1. Everything after that is yours.

`00_Setup_Data` already deployed **`falak-app`** in your workspace: an almost empty AppKit app (TypeScript + React) wired to your SQL warehouse, with read access to bronze, silver and gold. Its home page shows your lakehouse filling up as you build. The code is in [`app/`](../app); Claude Code reads its instructions from `app/CLAUDE.md`, and two tested pages are waiting in `app/examples/` (an Overview with KPIs and at-risk accounts, and an Ask Genie chat).

## 4.0 Before the hackathon (on your laptop)

- Node.js 22+ (`node --version`)
- Databricks CLI 1.17+ (`databricks --version`) → [install](https://docs.databricks.com/aws/en/dev-tools/cli/install)
- Claude Code (`claude --version`)
- Log the CLI in to your Free Edition workspace:
  ```bash
  databricks auth login --host https://<your-workspace>.cloud.databricks.com --profile hackathon
  ```
- Install the Databricks skills for Claude: `databricks aitools install`

## 4.1 Connect Claude to your app (1 minute)

```bash
git clone <this repo> && cd difc-hackathon-starter/app
npm install
claude
```

Then tell Claude:

```text
Connect to my app. My CLI profile is "hackathon".
```

Claude runs `node scripts/configure.mjs` and shows you the app URL. Then two quick wins, once your gold tables and Genie Agent exist:

```text
Add the Overview page from examples and make it the home page. Then connect my Genie Agent <paste the ID>
and add the Ask Genie page. Deploy.
```

## 4.2 Make it yours: prompts that work

Pick one idea per person and run them in parallel. Each one is a single prompt to Claude.

**Product ideas built on the data you already have:**

```text
Add a "Customer" page: when I click an at-risk account on the Overview, show its MRR history,
weekly usage trend, invoices and support tickets, plus the risk reasons as a banner.
```

```text
Add a "Retention playbook" button on each at-risk account that calls a chat foundation model available
in my workspace with the customer's context (from customer_360 and their last tickets) and drafts
a personal email from the account manager. Show the draft in a dialog with a copy button.
```

```text
Add a "Marketing" page with a bar chart of Return on Spend and CAC by acquisition channel
from the workspace.gold.acquisition_metrics metric view, and a short insight text on top.
```

```text
Add a "Support pulse" page: tickets per month by topic (stacked bar), median resolution hours and
average CSAT by topic, with a filter by country.
```

```text
Rebrand the app: name "Falak Command Center", a deep teal primary color, our logo text in the header,
and make the Overview the home page.
```

**Turn it into your startup:** swap Falak for your own business. Describe your product to Claude, ask it to rename the concepts (customers → patients, MRR → GMV...), and keep the same data plumbing.

## 4.3 Redeploy after each change

```text
Redeploy the app and check it is running.
```

Or `npm run deploy:app` from `app/` (about 2 minutes: it checks your code and SQL locally first, then uploads and deploys). Local preview without deploying: `npm run dev` then open http://localhost:8000.

## 4.4 Demo (2 minutes per team)

1. The problem in one sentence.
2. Live: one Genie question + one app feature.
3. What you would build next week.
