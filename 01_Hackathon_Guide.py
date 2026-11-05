# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-banner { display: flex; align-items: center; gap: 20px; width: 100%; border-radius: 10px; padding: 24px 28px; background: var(--bnr-bg); border-left: 8px solid var(--bnr-accent); box-shadow: 0 2px 10px rgba(27,49,57,0.08); }
# MAGIC .ds-banner-icon { width: 60px; height: 60px; border-radius: 50%; flex-shrink: 0; background: var(--bnr-accent); color: var(--bnr-icon-fg); font-size: 26pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; }
# MAGIC .ds-banner-title { font-size: 22pt; font-weight: 700; color: var(--bnr-title); line-height: 1.2; margin-bottom: 4px; }
# MAGIC .ds-banner-tagline { font-size: 15pt; color: var(--bnr-tagline); line-height: 1.4; }
# MAGIC .ds-banner.info { --bnr-bg: #1B5162; --bnr-accent: #4299E0; --bnr-icon-fg: #FFFFFF; --bnr-title: #FFFFFF; --bnr-tagline: #F9F7F4; }
# MAGIC .ds-banner.caution { --bnr-bg: rgba(255,171,0,0.12); --bnr-accent: #FFAB00; --bnr-icon-fg: #0b2026; --bnr-title: #0b2026; --bnr-tagline: #5E7077; }
# MAGIC .ds-banner.danger { --bnr-bg: rgba(255,95,70,0.10); --bnr-accent: #FF5F46; --bnr-icon-fg: #FFFFFF; --bnr-title: #98102A; --bnr-tagline: #5E7077; }
# MAGIC
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC
# MAGIC .flow-grid { display: grid; gap: 0; align-items: stretch; }
# MAGIC .flow-step { background: #F9F7F4; border: 3px solid var(--accent, #4299E0); border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0; }
# MAGIC .flow-num { font-size: 26pt; font-weight: 800; color: var(--accent, #4299E0); line-height: 1; margin-bottom: 8px; }
# MAGIC .flow-label { font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35; }
# MAGIC .flow-sub { font-size: 14pt; color: #5E7077; line-height: 1.35; margin-top: 6px; font-weight: 400; }
# MAGIC .flow-arrow { display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1; padding: 0 6px; }
# MAGIC .flow-step.dim { background: #EEEDE9; border-color: #C2C2C2; box-shadow: none; opacity: 0.7; }
# MAGIC .flow-step.dim .flow-num { color: #90A5B1; }
# MAGIC .flow-step.dim .flow-label, .flow-step.dim .flow-sub { color: #5A6F77; }
# MAGIC .flow-arrow.dim { color: #C2C2C2; }
# MAGIC </style>
# MAGIC <div class="ds-banner info"><div class="ds-banner-icon">F</div><div><div class="ds-banner-title">Falak Hackathon Guide</div><div class="ds-banner-tagline">From raw files to an AI-powered app in about an hour</div></div></div>
# MAGIC <div class="ds-callout caution row"><div class="ds-callout-icon">!</div><div><div class="ds-eyebrow">Do this first</div><div class="ds-callout-title">Run 00_Setup_Data now, then read on while it works (about 5 minutes)</div><div>It lands Falak's raw data in your workspace and deploys your starter app <code>falak-app</code>.</div></div></div>
# MAGIC <div class="flow-grid" style="grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#1B5162;"><div class="flow-num">1</div><div class="flow-label">Context</div><div class="flow-sub">Falak and its data</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">2</div><div class="flow-label">Pipeline</div><div class="flow-sub">Bronze, silver, gold</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">3</div><div class="flow-label">Metric views</div><div class="flow-sub">One definition per KPI</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">4</div><div class="flow-label">Genie Agent</div><div class="flow-sub">Ask the data</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">5</div><div class="flow-label">App</div><div class="flow-sub">Claude Code</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-row { display: flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 230px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;} .teal{--accent:#1B5162;}
# MAGIC .ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; }
# MAGIC .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-card-sub { font-size: 14pt; font-weight: 600; color: #1B5162; margin: 0 0 12px; line-height: 1.4; }
# MAGIC .ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
# MAGIC .ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; line-height: 1.4; }
# MAGIC .tc { text-align: center; }
# MAGIC
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC
# MAGIC .ds-band-solid { background: #1B5162; color: #fff; border-radius: 10px; padding: 22px 28px; text-align: center; border-top: 6px solid var(--accent, #FF5F46); box-shadow: 0 2px 10px rgba(27,49,57,0.12); }
# MAGIC .ds-band-lead { font-size: 17pt; font-weight: 700; color: #fff; line-height: 1.3; margin-bottom: 8px; }
# MAGIC .ds-band-sub { font-size: 14pt; color: #F9F7F4; font-weight: 600; line-height: 1.4; }
# MAGIC .ds-band-bordered { background: #F8F9FC; border: 3px solid #1B5162; border-radius: 8px; padding: 16px 24px; text-align: center; font-size: 16pt; color: #0b2026; line-height: 1.5; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">The context</div><div class="mh-title">Meet Falak</div><div class="mh-sub">A fictional Dubai startup: invoicing and payment links for SMEs across the GCC</div></div>
# MAGIC <div class="ds-row"><div class="ds-card blue tc"><div class="ds-stat">2,700</div><div class="ds-stat-label">paying SME customers</div></div><div class="ds-card green tc"><div class="ds-stat">2.0M AED</div><div class="ds-stat-label">monthly recurring revenue</div></div><div class="ds-card amber tc"><div class="ds-stat">6</div><div class="ds-stat-label">GCC countries, KSA launched Sep 2024</div></div><div class="ds-card coral tc"><div class="ds-stat">3 plans</div><div class="ds-stat-label">Starter, Growth, Scale, billed in AED, SAR or USD</div></div></div>
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">The situation</div><div class="ds-callout-title">Falak grew fast. The founders feel that something is off, but every team tells a different story.</div><ul><li>Marketing doubled the paid social budget in mid-2025. Was it worth it?</li><li>Churn jumped in late summer. Was it a one-off or a pattern?</li><li>The biggest accounts look fine on the CRM. Are they?</li></ul></div>
# MAGIC <div class="ds-band-solid" style="--accent:#FF5F46;"><div class="ds-band-lead">Your mission: find the problems hiding in the data, and build the tool the founders need to act on them.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-table { width: 100%; border-collapse: collapse; font-size: 14pt; background: #F9F7F4; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .ds-table th { text-align: left; background: #1B5162; color: #FFFFFF; font-weight: 700; padding: 10px 12px; }
# MAGIC .ds-table td { padding: 9px 12px; border-bottom: 1px solid #EEEDE9; vertical-align: top; line-height: 1.45; }
# MAGIC .ds-table tr:nth-child(even) td { background: #FFFFFF; }
# MAGIC .ds-table td.k { font-weight: 700; white-space: nowrap; }
# MAGIC .ds-table td.mono, .ds-table span.mono { font-family: Menlo, Consolas, monospace; font-size: 14pt; }
# MAGIC
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">What you start with</div><div class="mh-title">The raw data</div><div class="mh-sub">Six source systems, delivered as files in a Unity Catalog volume: /Volumes/workspace/raw/landing/</div></div>
# MAGIC <table class="ds-table"><thead><tr><th>Source system</th><th>Folder</th><th>Format</th><th>Rows</th><th>What is inside</th></tr></thead><tbody><tr><td class="k">CRM export</td><td class="mono">crm/</td><td>CSV</td><td>~4.1k</td><td>Customers: company, industry, country, size, acquisition channel, account manager</td></tr><tr><td class="k">Billing: subscriptions</td><td class="mono">billing/subscription_events/</td><td>JSON, nested <code>plan</code></td><td>~8.5k</td><td>New, upgrade, downgrade, seat change, churn, reactivation, with MRR</td></tr><tr><td class="k">Billing: invoices</td><td class="mono">billing/invoices/</td><td>JSON</td><td>~34k</td><td>Monthly invoices, status, payment method, attempts</td></tr><tr><td class="k">Product analytics</td><td class="mono">product_events/</td><td>JSON, nested <code>context</code></td><td>~1.0M</td><td>Logins, invoices created, payment links sent or failed, integrations</td></tr><tr><td class="k">Support desk</td><td class="mono">support/tickets/</td><td>JSON, free text</td><td>~5.3k</td><td>Subject and description in English and Arabic, CSAT</td></tr><tr><td class="k">Marketing</td><td class="mono">marketing/</td><td>CSV</td><td>204</td><td>Monthly spend, clicks and leads per channel</td></tr><tr><td class="k">Finance</td><td class="mono">reference/</td><td>CSV</td><td>105</td><td>Monthly FX rates to AED</td></tr></tbody></table>
# MAGIC <div class="ds-callout caution row"><div class="ds-callout-icon">!</div><div><div class="ds-eyebrow">Heads up</div><div>The data is messy on purpose, like real exports: duplicates, QA test accounts, a country spelled five ways, three date formats, three currencies, statuses in mixed case. Cleaning it is part of the job.</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .flow-grid { display: grid; gap: 0; align-items: stretch; }
# MAGIC .flow-step { background: #F9F7F4; border: 3px solid var(--accent, #4299E0); border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0; }
# MAGIC .flow-num { font-size: 26pt; font-weight: 800; color: var(--accent, #4299E0); line-height: 1; margin-bottom: 8px; }
# MAGIC .flow-label { font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35; }
# MAGIC .flow-sub { font-size: 14pt; color: #5E7077; line-height: 1.35; margin-top: 6px; font-weight: 400; }
# MAGIC .flow-arrow { display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1; padding: 0 6px; }
# MAGIC .flow-step.dim { background: #EEEDE9; border-color: #C2C2C2; box-shadow: none; opacity: 0.7; }
# MAGIC .flow-step.dim .flow-num { color: #90A5B1; }
# MAGIC .flow-step.dim .flow-label, .flow-step.dim .flow-sub { color: #5A6F77; }
# MAGIC .flow-arrow.dim { color: #C2C2C2; }
# MAGIC
# MAGIC .ds-table { width: 100%; border-collapse: collapse; font-size: 14pt; background: #F9F7F4; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .ds-table th { text-align: left; background: #1B5162; color: #FFFFFF; font-weight: 700; padding: 10px 12px; }
# MAGIC .ds-table td { padding: 9px 12px; border-bottom: 1px solid #EEEDE9; vertical-align: top; line-height: 1.45; }
# MAGIC .ds-table tr:nth-child(even) td { background: #FFFFFF; }
# MAGIC .ds-table td.k { font-weight: 700; white-space: nowrap; }
# MAGIC .ds-table td.mono, .ds-table span.mono { font-family: Menlo, Consolas, monospace; font-size: 14pt; }
# MAGIC
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">The plan</div><div class="mh-title">What you will build</div><div class="mh-sub">Four steps, each with a copy-paste prompt. The app is already deployed and waiting.</div></div>
# MAGIC <div class="flow-grid" style="grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr auto 1fr;"><div class="flow-step" style="--accent:#1B5162;"><div class="flow-num">1</div><div class="flow-label">Raw files</div><div class="flow-sub">volume</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FFAB00;"><div class="flow-num">2</div><div class="flow-label">Bronze</div><div class="flow-sub">ingest as-is</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#4299E0;"><div class="flow-num">3</div><div class="flow-label">Silver</div><div class="flow-sub">clean and conform</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">4</div><div class="flow-label">Gold</div><div class="flow-sub">business tables</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#00A972;"><div class="flow-num">5</div><div class="flow-label">Metric views</div><div class="flow-sub">governed KPIs</div></div><div class="flow-arrow">&rarr;</div><div class="flow-step" style="--accent:#FF5F46;"><div class="flow-num">6</div><div class="flow-label">Genie + App</div><div class="flow-sub">answers and actions</div></div></div>
# MAGIC <table class="ds-table"><thead><tr><th>Step</th><th>You build</th><th>Tool</th><th>Time</th></tr></thead><tbody><tr><td class="k">1</td><td>A Lakeflow Spark Declarative Pipeline: 7 bronze, 7 silver, 4 gold tables</td><td>Genie Code in the Lakeflow Pipelines Editor</td><td>25 min</td></tr><tr><td class="k">2</td><td>Two metric views: revenue and acquisition</td><td>Genie Code in the SQL editor</td><td>10 min</td></tr><tr><td class="k">3</td><td>A Genie Agent that answers business questions correctly</td><td>Genie</td><td>10 min</td></tr><tr><td class="k">4</td><td>Your product on top of <code>falak-app</code></td><td>Claude Code on your laptop (<code>guides/4_App_with_Claude.md</code>)</td><td>25 min</td></tr></tbody></table>
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Behind schedule?</div><div>Run <code>99_Catch_Up</code>: it builds the reference pipeline and the metric views in about 3 minutes. Then jump to step 3.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .fc-row { display: flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .fc-row > .fc-card { flex: 1; min-width: 300px; }
# MAGIC .fc-card { background: #F9F7F4; border-radius: 10px; padding: 20px; border-top: 8px solid var(--accent); box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .fc-title { font-size: 18pt; font-weight: 700; color: #0b2026; margin-bottom: 12px; }
# MAGIC .fc-intro { font-size: 14pt; line-height: 1.55; color: #0b2026; margin-bottom: 14px; }
# MAGIC .fc-item { display: grid; grid-template-columns: 210px 1fr; gap: 20px; padding: 12px 0; border-bottom: 1px solid #EEEDE9; align-items: start; }
# MAGIC .fc-item:first-child { padding-top: 4px; }
# MAGIC .fc-item:last-child { border-bottom: none; padding-bottom: 4px; }
# MAGIC .fc-key { font-size: 14pt; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; line-height: 1.3; color: var(--accent); }
# MAGIC .fc-val { font-size: 14pt; color: #0b2026; line-height: 1.55; }
# MAGIC .fc-val ul { margin: 0; padding-left: 18px; }
# MAGIC .fc-val li { margin-bottom: 6px; }
# MAGIC .fc-example { margin-top: 14px; border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0; padding: 14px 16px; font-size: 14pt; line-height: 1.55; background: var(--tint); }
# MAGIC .fc-example strong:first-child { text-transform: uppercase; font-size: 14pt; letter-spacing: 1.5px; display: block; margin-bottom: 6px; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1 · Concept</div><div class="mh-title">The medallion architecture</div><div class="mh-sub">Three layers, three contracts. Quality and business value increase at every step.</div></div>
# MAGIC <div class="fc-row"><div class="fc-card" style="--accent:#FFAB00; --tint:rgba(255,171,0,0.12);"><div class="fc-title">Bronze: keep everything</div><div><div class="fc-item"><div class="fc-key">Contract</div><div class="fc-val">Exactly what the source sent, plus where and when it arrived</div></div><div class="fc-item"><div class="fc-key">Why</div><div class="fc-val">Replay history, audit, fix a bug without asking the source again</div></div><div class="fc-item"><div class="fc-key">Falak</div><div class="fc-val"><code>bronze.product_events</code> keeps the duplicate events</div></div></div></div><div class="fc-card" style="--accent:#4299E0; --tint:rgba(66,153,224,0.10);"><div class="fc-title">Silver: clean and conform</div><div><div class="fc-item"><div class="fc-key">Contract</div><div class="fc-val">One trustworthy, typed, deduplicated version of each entity</div></div><div class="fc-item"><div class="fc-key">Why</div><div class="fc-val">Every team starts from the same clean customers, invoices, events</div></div><div class="fc-item"><div class="fc-key">Falak</div><div class="fc-val"><code>silver.customers</code>: no test accounts, one country spelling</div></div></div></div><div class="fc-card" style="--accent:#00A972; --tint:rgba(0,169,114,0.10);"><div class="fc-title">Gold: ready for the business</div><div><div class="fc-item"><div class="fc-key">Contract</div><div class="fc-val">Facts and aggregates shaped for a question or a product</div></div><div class="fc-item"><div class="fc-key">Why</div><div class="fc-val">Fast, simple to query for people, Genie and apps</div></div><div class="fc-item"><div class="fc-key">Falak</div><div class="fc-val"><code>gold.customer_360</code>: one row per customer with a risk level</div></div></div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-row { display: flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 230px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;} .teal{--accent:#1B5162;}
# MAGIC .ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; }
# MAGIC .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-card-sub { font-size: 14pt; font-weight: 600; color: #1B5162; margin: 0 0 12px; line-height: 1.4; }
# MAGIC .ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
# MAGIC .ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; line-height: 1.4; }
# MAGIC .tc { text-align: center; }
# MAGIC
# MAGIC .dd-head { font-size: 20pt; font-weight: 700; margin: 4px 0 12px; color: var(--accent); }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1 · Concept</div><div class="mh-title">Lakeflow Spark Declarative Pipelines</div><div class="mh-sub">You declare the tables you want. The pipeline works out the order, the compute and the incremental updates.</div></div>
# MAGIC <div class="ds-row"><div class="ds-card amber"><div class="ds-card-label">Bronze</div><div class="ds-card-title">Streaming table</div><div class="ds-card-para"><code>CREATE OR REFRESH STREAMING TABLE ... FROM STREAM read_files(...)</code>. Reads only the new files on each update (Auto Loader).</div></div><div class="ds-card blue"><div class="ds-card-label">Silver and gold</div><div class="ds-card-title">Materialized view</div><div class="ds-card-para"><code>CREATE OR REFRESH MATERIALIZED VIEW ... AS SELECT ...</code>. The result of a query, kept up to date by the pipeline.</div></div><div class="ds-card green"><div class="ds-card-label">Quality</div><div class="ds-card-title">Expectations</div><div class="ds-card-para"><code>CONSTRAINT valid_id EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW</code>. Tracked on every update.</div></div></div>
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="dd-head">&check; DO</div><ul><li>One SQL file per layer: <code>01_bronze.sql</code>, <code>02_silver.sql</code>, <code>03_gold.sql</code></li><li>Refer to tables as <code>bronze.x</code>, <code>silver.x</code>, <code>gold.x</code> inside the pipeline</li><li>Run the pipeline after each layer and look at the graph</li></ul></div><div class="ds-card coral"><div class="dd-head">&times; DON'T</div><ul><li>Clean data in bronze</li><li>Hard-code row counts or dates you saw today</li><li>Skip the data quality tab: it is where the traps show up</li></ul></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-steps { display: flex; flex-direction: column; gap: 20px; }
# MAGIC .ds-step { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 18px 20px; border-top: 6px solid var(--accent, #4299E0); }
# MAGIC .ds-step.blue { --accent:#4299E0; --tint:rgba(66,153,224,0.10); }
# MAGIC .ds-step.green { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-step.amber { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-step.coral { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-step.red { --accent:#98102A; --tint:rgba(152,16,42,0.10); }
# MAGIC .ds-step.teal { --accent:#1B5162; --tint:rgba(27,81,98,0.10); }
# MAGIC .ds-step-head { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
# MAGIC .ds-step-num { width: 36px; height: 36px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 18pt; font-weight: 800; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-step-title { font-size: 18pt; font-weight: 700; color: #0b2026; }
# MAGIC .ds-step-text { font-size: 14pt; color: #0b2026; line-height: 1.6; }
# MAGIC .ds-step-text ul { margin: 0; padding-left: 20px; }
# MAGIC .ds-step-text li { margin-bottom: 8px; }
# MAGIC .ds-example { margin-top: 12px; padding: 10px 12px; border-radius: 8px; font-size: 14pt; line-height: 1.5; background: var(--tint); border-left: 4px solid var(--accent); }
# MAGIC .ds-example ul { margin: 4px 0 0; padding-left: 18px; }
# MAGIC .ds-example li { margin-bottom: 4px; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1.0</div><div class="mh-title">Set up Genie Code (1 minute, once)</div><div class="mh-sub">Genie Code is the AI assistant built into Databricks. It writes, runs and fixes code for you.</div></div>
# MAGIC <div class="ds-steps"><div class="ds-step blue"><div class="ds-step-head"><div class="ds-step-num">1</div><div class="ds-step-title">Open Genie Code</div></div><div class="ds-step-text"><div>Click the <strong>sparkle icon</strong> at the top right of most pages.</div></div></div><div class="ds-step green"><div class="ds-step-head"><div class="ds-step-num">2</div><div class="ds-step-title">Give it the project context</div></div><div class="ds-step-text"><div><strong>More</strong> menu → <strong>Customizations</strong> → <strong>Instructions</strong> → paste the block below and save.</div></div></div><div class="ds-step amber"><div class="ds-step-head"><div class="ds-step-num">3</div><div class="ds-step-title">Done</div></div><div class="ds-step-text"><div>Every prompt in this guide now knows Falak, the folder layout and the naming rules.</div></div></div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Genie Code instructions</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">You are helping a startup founder at a 1-hour Databricks hackathon. Be fast, write working code, run it, fix errors yourself.
# MAGIC
# MAGIC Project: Falak, a fictional Dubai startup selling invoicing and payment-link software to SMEs in the GCC (UAE, KSA, Qatar, Bahrain, Oman, Kuwait). Plans: Starter, Growth, Scale. Currencies AED, SAR, USD. Report money in AED.
# MAGIC
# MAGIC Data layout (Unity Catalog, catalog `workspace`):
# MAGIC - Raw files: /Volumes/workspace/raw/landing/ with folders crm/, billing/subscription_events/, billing/invoices/, product_events/, support/tickets/, marketing/, reference/
# MAGIC - Schemas: bronze (raw as-is), silver (clean), gold (business tables)
# MAGIC - Gold contract used by the app: gold.mrr_monthly, gold.customer_360, gold.acquisition_monthly, gold.support_tickets
# MAGIC
# MAGIC Rules:
# MAGIC - Pipelines are Lakeflow Spark Declarative Pipelines in SQL. Bronze = STREAMING TABLE with STREAM read_files on a folder. Silver and gold = MATERIALIZED VIEW.
# MAGIC - Always use two-part names in pipeline code (bronze.x, silver.x, gold.x) and three-part names elsewhere (workspace.gold.x).
# MAGIC - One SQL file per layer: 01_bronze.sql, 02_silver.sql, 03_gold.sql.
# MAGIC - Add a COMMENT to every table. Use expectations (CONSTRAINT ... EXPECT) for data quality in silver.
# MAGIC - Use serverless compute. Keep queries simple and readable, this code will be shown on stage.</pre></div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-steps { display: flex; flex-direction: column; gap: 20px; }
# MAGIC .ds-step { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 18px 20px; border-top: 6px solid var(--accent, #4299E0); }
# MAGIC .ds-step.blue { --accent:#4299E0; --tint:rgba(66,153,224,0.10); }
# MAGIC .ds-step.green { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-step.amber { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-step.coral { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-step.red { --accent:#98102A; --tint:rgba(152,16,42,0.10); }
# MAGIC .ds-step.teal { --accent:#1B5162; --tint:rgba(27,81,98,0.10); }
# MAGIC .ds-step-head { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
# MAGIC .ds-step-num { width: 36px; height: 36px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 18pt; font-weight: 800; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-step-title { font-size: 18pt; font-weight: 700; color: #0b2026; }
# MAGIC .ds-step-text { font-size: 14pt; color: #0b2026; line-height: 1.6; }
# MAGIC .ds-step-text ul { margin: 0; padding-left: 20px; }
# MAGIC .ds-step-text li { margin-bottom: 8px; }
# MAGIC .ds-example { margin-top: 12px; padding: 10px 12px; border-radius: 8px; font-size: 14pt; line-height: 1.5; background: var(--tint); border-left: 4px solid var(--accent); }
# MAGIC .ds-example ul { margin: 4px 0 0; padding-left: 18px; }
# MAGIC .ds-example li { margin-bottom: 4px; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1.1</div><div class="mh-title">Create the pipeline (2 minutes)</div><div class="mh-sub">One pipeline builds all three layers</div></div>
# MAGIC <div class="ds-steps"><div class="ds-step blue"><div class="ds-step-head"><div class="ds-step-num">1</div><div class="ds-step-title">New → ETL pipeline</div></div><div class="ds-step-text"><div>Opens the Lakeflow Pipelines Editor.</div></div></div><div class="ds-step green"><div class="ds-step-head"><div class="ds-step-num">2</div><div class="ds-step-title">Settings</div></div><div class="ds-step-text"><ul><li>Name: <code>falak_pipeline</code></li><li>Default catalog: <code>workspace</code>, default schema: <code>bronze</code></li><li>Language: <strong>SQL</strong>, start from an <strong>empty file</strong></li></ul></div></div><div class="ds-step amber"><div class="ds-step-head"><div class="ds-step-num">3</div><div class="ds-step-title">Open Genie Code from inside the editor</div></div><div class="ds-step-text"><div>So it creates and edits the pipeline files directly. Paste the prompts below one at a time, and click <strong>Run pipeline</strong> after each.</div></div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1.2</div><div class="mh-title">Bronze: ingest everything, as delivered</div><div class="mh-sub">7 streaming tables, one per source folder</div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt: bronze</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">In this pipeline, create the file 01_bronze.sql with one streaming table per source.
# MAGIC Use STREAM read_files on these folders of /Volumes/workspace/raw/landing/ :
# MAGIC
# MAGIC - bronze.crm_customers        &lt;- crm/                           (format csv, header true)
# MAGIC - bronze.subscription_events  &lt;- billing/subscription_events/   (format json)
# MAGIC - bronze.invoices             &lt;- billing/invoices/              (format json, schemaHints 'amount STRING')
# MAGIC - bronze.product_events       &lt;- product_events/                (format json)
# MAGIC - bronze.support_tickets      &lt;- support/tickets/               (format json)
# MAGIC - bronze.marketing_spend      &lt;- marketing/                     (format csv, header true)
# MAGIC - bronze.fx_rates             &lt;- reference/                     (format csv, header true)
# MAGIC
# MAGIC Keep every column as delivered, do not clean anything. Add two columns to each table:
# MAGIC source_file (from _metadata.file_path) and ingested_at (current_timestamp()).
# MAGIC Add a one-line COMMENT on each table describing the source system.</pre></div>

# COMMAND ----------

# MAGIC %md
# MAGIC **Check:** run the pipeline. You should see 7 tables in the graph, `product_events` around 1M rows. Then run this cell.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'crm_customers' AS table_name, count(*) AS row_count FROM workspace.bronze.crm_customers
# MAGIC UNION ALL SELECT 'subscription_events', count(*) FROM workspace.bronze.subscription_events
# MAGIC UNION ALL SELECT 'invoices', count(*) FROM workspace.bronze.invoices
# MAGIC UNION ALL SELECT 'product_events', count(*) FROM workspace.bronze.product_events
# MAGIC UNION ALL SELECT 'support_tickets', count(*) FROM workspace.bronze.support_tickets
# MAGIC UNION ALL SELECT 'marketing_spend', count(*) FROM workspace.bronze.marketing_spend
# MAGIC UNION ALL SELECT 'fx_rates', count(*) FROM workspace.bronze.fx_rates

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1.3</div><div class="mh-title">Play detective before cleaning (optional, 3 minutes)</div><div class="mh-sub">The best data engineers look before they clean. Compare with the spoiler in the notes below.</div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt: data quality detective</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Profile the 7 bronze tables and list every data quality problem you find:
# MAGIC duplicates, test or fake records, inconsistent values, mixed date or timestamp formats,
# MAGIC wrong types, nested fields, codes that do not match between tables.
# MAGIC Answer with a table: bronze table | problem | example value | how to fix it in silver.</pre></div>
# MAGIC
# MAGIC ##### EXPAND FOR ADDITIONAL NOTES
# MAGIC
# MAGIC <details>
# MAGIC
# MAGIC ### Spoiler: what is wrong with the data
# MAGIC
# MAGIC | Table | Problem |
# MAGIC |---|---|
# MAGIC | crm_customers | duplicated customers (keep the latest `last_modified`), 12 QA test accounts (`TEST ACCOUNT ...`, `@falak.io`), country spelled 5 ways, 3 date formats in `signup_date`, trailing spaces, missing industry |
# MAGIC | subscription_events | nested `plan` struct, MRR in AED, SAR or USD, test accounts with MRR 0 |
# MAGIC | invoices | `status` in mixed case, `amount` sometimes a string, three currencies |
# MAGIC | product_events | ~1% duplicate `event_id`, two timestamp formats, nested `context` and `properties` |
# MAGIC | support_tickets | English and Arabic free text, inconsistent `status`, `agent_category` filled 40% of the time |
# MAGIC | marketing_spend | channel codes (`paid_social`) differ from CRM labels (`Paid Social`) |
# MAGIC | fx_rates | `month` looks like `2024-01` but is inferred as a DATE |
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1.4</div><div class="mh-title">Silver: clean, type, deduplicate</div><div class="mh-sub">7 materialized views with data quality expectations</div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt: silver</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Create the file 02_silver.sql with one MATERIALIZED VIEW per entity, in the silver schema.
# MAGIC
# MAGIC 1. silver.fx_rates: month (DATE), currency (upper case), rate_to_aed (DOUBLE).
# MAGIC    The CSV month may already be inferred as a DATE: use to_date(substr(CAST(month AS STRING), 1, 7), 'yyyy-MM').
# MAGIC
# MAGIC 2. silver.customers: one row per customer_id, keeping the row with the latest last_modified.
# MAGIC    - remove QA test accounts: company_name starting with 'TEST ACCOUNT' or contact_email ending with '@falak.io'
# MAGIC    - trim company_name; industry NULL becomes 'Unknown'
# MAGIC    - country to full names: UAE, U.A.E., AE, uae -&gt; United Arab Emirates; KSA, SA, Kingdom of Saudi Arabia -&gt; Saudi Arabia;
# MAGIC      QA -&gt; Qatar; BH -&gt; Bahrain; OM -&gt; Oman; KW -&gt; Kuwait
# MAGIC    - signup_date as DATE from three formats: yyyy-MM-dd, dd/MM/yyyy and MMM dd, yyyy (use try_to_date + coalesce)
# MAGIC    - expectations: customer_id IS NOT NULL (drop row), signup_date IS NOT NULL, country in the 6 full names
# MAGIC
# MAGIC 3. silver.subscription_events: flatten the plan struct into plan_name, seats (INT), mrr (DOUBLE), currency;
# MAGIC    effective_at as TIMESTAMP; mrr_aed = mrr x rate_to_aed, joining silver.fx_rates on currency and the month of effective_at.
# MAGIC    Inner join silver.customers to keep real customers only.
# MAGIC    Expectations: event_type in (new, upgrade, downgrade, seat_change, churn, reactivation), mrr &gt;= 0, mrr_aed IS NOT NULL.
# MAGIC
# MAGIC 4. silver.invoices: issued_at and paid_at as TIMESTAMP, due_date as DATE, amount as DOUBLE (it is sometimes a string),
# MAGIC    status lower-cased and trimmed, amount_aed via silver.fx_rates (month of issued_at). Real customers only.
# MAGIC    Expectations: amount &gt; 0 (drop row), status in (paid, failed, overdue, pending, refunded), amount_aed IS NOT NULL.
# MAGIC
# MAGIC 5. silver.product_events: deduplicate on event_id (QUALIFY row_number() OVER (PARTITION BY event_id ORDER BY ingested_at) = 1),
# MAGIC    event_ts as TIMESTAMP (two formats exist, CAST handles both), flatten context into platform, app_version, locale and
# MAGIC    properties into amount, integration, error_code, report_type. Expectation: event_ts IS NOT NULL (drop row).
# MAGIC
# MAGIC 6. silver.support_tickets: created_at and resolved_at as TIMESTAMP, status 'resolved' or 'closed' (any case) -&gt; 'closed',
# MAGIC    otherwise lower-cased; csat_score INT; keep agent_category as agent_category_raw; exclude customer_id starting with 'C-9'.
# MAGIC    Add a topic column from the subject, checked in this order (subjects can be Arabic):
# MAGIC    cancellation (cancel, alternatives, or Arabic إلغاء) ; feature_request (arabic invoice, whatsapp, multi-currency, or ميزة) ;
# MAGIC    onboarding (import, template, adding my team, or شعار) ; payment_failure (payment link, declined, stuck in processing, or الدفع) ;
# MAGIC    e_invoicing (e-invoic, zatca, or فاتورة) ; integration_sync (sync, connection, not showing in) ;
# MAGIC    billing_question (charged, seats, tax invoice, annual billing) ; otherwise how_to.
# MAGIC
# MAGIC 7. silver.marketing_spend: month as DATE (same trick as fx_rates), map channel codes to CRM names:
# MAGIC    paid_social -&gt; Paid Social, google_ads -&gt; Google Ads, seo_content -&gt; Organic, referral_program -&gt; Referral,
# MAGIC    bank_partnership -&gt; Partner Bank, events -&gt; Events. spend_aed DOUBLE, impressions, clicks and leads BIGINT.
# MAGIC
# MAGIC Add a COMMENT to every table.</pre></div>

# COMMAND ----------

# MAGIC %md
# MAGIC **Check:** run the pipeline, open each silver table in the graph and look at its **data quality** tab. Then run this cell: about 3,970 customers (from ~4,100 CRM rows), 6 countries, about 1.02M events (from ~1.03M), and 0 events missing an FX rate.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT count(*) FROM workspace.bronze.crm_customers) AS crm_rows,
# MAGIC   (SELECT count(*) FROM workspace.silver.customers) AS customers,
# MAGIC   (SELECT count(DISTINCT country) FROM workspace.silver.customers) AS countries,
# MAGIC   (SELECT count(*) FROM workspace.bronze.product_events) AS raw_events,
# MAGIC   (SELECT count(*) FROM workspace.silver.product_events) AS events,
# MAGIC   (SELECT count_if(mrr_aed IS NULL) FROM workspace.silver.subscription_events) AS events_missing_fx

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1.5</div><div class="mh-title">Gold: the tables your app and Genie use</div><div class="mh-sub">4 materialized views. Keep the names and columns: the starter app examples read them.</div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt: gold</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Create the file 03_gold.sql with these MATERIALIZED VIEWS in the gold schema.
# MAGIC Keep the names and columns exactly: the app and Genie use them.
# MAGIC
# MAGIC 1. gold.mrr_monthly: one row per customer per month.
# MAGIC    - month spine: from the month of each customer's first subscription event to the latest month in silver.subscription_events
# MAGIC    - state at month end = the latest subscription event with effective_at before the next month (max_by): mrr_aed, plan_name, seats
# MAGIC    - prev_mrr_aed = previous month's mrr_aed (0 if none); is_active = mrr_aed &gt; 0
# MAGIC    - movement: new (first month, prev 0), reactivation (prev 0, not first month), churn (prev &gt; 0, now 0),
# MAGIC      expansion (mrr up), contraction (mrr down, still &gt; 0), flat
# MAGIC    - new_mrr_aed, reactivation_mrr_aed, expansion_mrr_aed, contraction_mrr_aed, churned_mrr_aed (the MRR amount of that movement)
# MAGIC    - add company_name, country, industry, company_size, acquisition_channel and signup_cohort (signup month) from silver.customers
# MAGIC    - keep only rows where mrr_aed &gt; 0 or prev_mrr_aed &gt; 0
# MAGIC
# MAGIC 2. gold.customer_360: one row per customer. as_of_date = CAST(max(event_ts) AS DATE) from silver.product_events ("today").
# MAGIC    - profile: customer_id, company_name, industry, country, city, company_size, acquisition_channel, account_manager, signup_date
# MAGIC    - from the latest subscription event: status ('churned' if it is a churn, else 'active'), churn_date, plan_name, seats,
# MAGIC      billing_cycle, mrr_aed (0 if churned); tenure_months = months between signup_date and as_of_date
# MAGIC    - activated_14d: an integration_connected event within 14 days of signup_date; integration = the first one connected
# MAGIC    - events_last_30d (event_ts &gt;= as_of_date - 29 days), events_prev_30d (the 30 days before that),
# MAGIC      usage_change_pct = 100 x (last - prev) / prev, payment_link_failures_90d
# MAGIC    - failed_invoices_90d (status failed, issued in the last 90 days), unpaid_amount_aed (failed, overdue, pending)
# MAGIC    - tickets_90d, open_tickets (open or pending), cancellation_tickets_90d, last_ticket_subject
# MAGIC    - risk_level, for active customers only:
# MAGIC      high   = (events_prev_30d &gt;= 5 and usage_change_pct &lt;= -50) or failed_invoices_90d &gt;= 2 or cancellation_tickets_90d &gt; 0
# MAGIC      medium = usage_change_pct &lt;= -30 or failed_invoices_90d &gt;= 1 or open_tickets &gt;= 2
# MAGIC      low    = everything else
# MAGIC    - risk_reasons: a readable sentence, for example 'usage down 61% vs previous 30 days; 2 failed invoice(s) in 90 days'
# MAGIC
# MAGIC 3. gold.acquisition_monthly: month x acquisition_channel, full outer join of
# MAGIC    signups from gold.customer_360 (signups, activated_signups, churned_to_date, by signup month and channel) and
# MAGIC    silver.marketing_spend (spend_aed, leads, clicks), plus revenue_to_date_aed = sum of mrr_aed in gold.mrr_monthly
# MAGIC    for that signup_cohort and channel.
# MAGIC
# MAGIC 4. gold.support_tickets: silver.support_tickets joined with silver.customers (company_name, country, company_size,
# MAGIC    acquisition_channel), plus created_month and resolution_hours.
# MAGIC
# MAGIC Add a COMMENT to every table, and column comments on the non-obvious columns.</pre></div>

# COMMAND ----------

# MAGIC %md
# MAGIC **Check:** run the pipeline (4 gold tables appear), then run the two cells below.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- October 2026 should be close to 2.0M AED and ~2,700 active customers
# MAGIC SELECT month, round(sum(mrr_aed)) AS mrr_aed, count_if(is_active) AS active_customers
# MAGIC FROM workspace.gold.mrr_monthly GROUP BY month ORDER BY month DESC LIMIT 6

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Rimal Logistics Co. should be at the top
# MAGIC SELECT company_name, country, plan_name, mrr_aed, risk_reasons
# MAGIC FROM workspace.gold.customer_360 WHERE status = 'active' AND risk_level = 'high'
# MAGIC ORDER BY mrr_aed DESC LIMIT 10

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-row { display: flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 230px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;} .teal{--accent:#1B5162;}
# MAGIC .ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; }
# MAGIC .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-card-sub { font-size: 14pt; font-weight: 600; color: #1B5162; margin: 0 0 12px; line-height: 1.4; }
# MAGIC .ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
# MAGIC .ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; line-height: 1.4; }
# MAGIC .tc { text-align: center; }
# MAGIC
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 1.6</div><div class="mh-title">Stretch goals for step 1</div><div class="mh-sub">If you are ahead, pick one</div></div>
# MAGIC <div class="ds-row"><div class="ds-card coral"><div class="ds-card-title">AI Functions</div><div class="ds-card-text">Ask Genie Code to replace the rule-based ticket topic with <code>ai_classify(description, ARRAY(...))</code>, or add <code>ai_analyze_sentiment</code>.</div></div><div class="ds-card blue"><div class="ds-card-title">Incremental</div><div class="ds-card-text">Run <code>02_New_Data_Drop</code>, refresh the pipeline, and check how many rows each streaming table processed.</div></div><div class="ds-card green"><div class="ds-card-title">AUTO CDC</div><div class="ds-card-text">Rebuild <code>silver.customers</code> with <code>AUTO CDC INTO ... KEYS (customer_id) SEQUENCE BY last_modified</code>.</div></div></div>
# MAGIC <div class="ds-callout caution row"><div class="ds-callout-icon">!</div><div><div class="ds-eyebrow">Behind at minute 25?</div><div>Stop your pipeline and run <code>99_Catch_Up</code>. Same gold tables in about 3 minutes.</div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-row { display: flex; gap: 22px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 230px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;} .teal{--accent:#1B5162;}
# MAGIC .ds-card-title { font-size: 18pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; }
# MAGIC .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-card-sub { font-size: 14pt; font-weight: 600; color: #1B5162; margin: 0 0 12px; line-height: 1.4; }
# MAGIC .ds-stat { font-size: 26pt; font-weight: 800; color: var(--accent); line-height: 1.1; }
# MAGIC .ds-stat-label { font-size: 14pt; color: #5E7077; margin-top: 6px; line-height: 1.4; }
# MAGIC .tc { text-align: center; }
# MAGIC
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 2 · Concept</div><div class="mh-title">Metric views: define each KPI once</div><div class="mh-sub">Ask three people for the churn rate and you get three numbers. A metric view ends that.</div></div>
# MAGIC <div class="ds-row"><div class="ds-card green"><div class="ds-card-label">Measures</div><div class="ds-card-title">The formulas</div><div class="ds-card-para">MRR, churn rate, CAC, return on spend. Written once, in YAML, governed in Unity Catalog.</div></div><div class="ds-card blue"><div class="ds-card-label">Dimensions</div><div class="ds-card-title">The ways to slice</div><div class="ds-card-para">Month, country, channel, plan. Any measure works with any dimension, no SQL rewrite.</div></div><div class="ds-card coral"><div class="ds-card-label">Consumers</div><div class="ds-card-title">Everyone agrees</div><div class="ds-card-para">Genie, AI/BI dashboards, your app and SQL all use <code>MEASURE(`MRR`)</code> and get the same number.</div></div></div>
# MAGIC <div class="ds-callout info"><div class="ds-eyebrow">How</div><div>Open a <strong>SQL editor</strong> tab, open Genie Code there and paste the prompts below.</div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 2.1</div><div class="mh-title">Revenue metrics</div><div class="mh-sub">On gold.mrr_monthly</div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt: revenue metric view</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Create a Unity Catalog metric view workspace.gold.revenue_metrics on workspace.gold.mrr_monthly
# MAGIC (CREATE OR REPLACE VIEW ... WITH METRICS LANGUAGE YAML, version 1.1), and run it.
# MAGIC
# MAGIC Dimensions: Month, Country, Industry, Company Size, Acquisition Channel, Plan (plan_name), Signup Cohort, Movement.
# MAGIC Measures:
# MAGIC - MRR = SUM(mrr_aed)
# MAGIC - Active Customers = COUNT(DISTINCT customer_id) where is_active
# MAGIC - ARPA = MRR / Active Customers
# MAGIC - New MRR, Expansion MRR, Contraction MRR, Churned MRR, Reactivation MRR = SUM of the matching column
# MAGIC - Net New MRR = new + expansion + reactivation - contraction - churned
# MAGIC - Churned Customers = COUNT(DISTINCT customer_id) where movement = 'churn'
# MAGIC - Logo Churn Rate = Churned Customers / COUNT(DISTINCT customer_id) where prev_mrr_aed &gt; 0
# MAGIC - Net Revenue Retention = SUM(mrr_aed where prev_mrr_aed &gt; 0) / SUM(prev_mrr_aed)
# MAGIC
# MAGIC Add a view comment saying MRR is a monthly snapshot and must always be sliced by Month.
# MAGIC Add synonyms: MRR -&gt; monthly recurring revenue, revenue; Logo Churn Rate -&gt; churn rate; Net Revenue Retention -&gt; NRR;
# MAGIC Acquisition Channel -&gt; channel, marketing channel.</pre></div>

# COMMAND ----------

# MAGIC %md
# MAGIC **Check:** October 2026 should show about 2.0M AED of MRR, and churn should spike in August.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT `Month`, MEASURE(`MRR`) AS mrr_aed, MEASURE(`Active Customers`) AS active_customers,
# MAGIC        MEASURE(`Logo Churn Rate`) AS churn_rate, MEASURE(`Net Revenue Retention`) AS nrr
# MAGIC FROM workspace.gold.revenue_metrics
# MAGIC WHERE `Month` >= '2026-01-01'
# MAGIC GROUP BY ALL ORDER BY `Month`

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 2.2</div><div class="mh-title">Acquisition metrics</div><div class="mh-sub">On gold.acquisition_monthly. This one tells Falak's whole marketing story.</div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt: acquisition metric view</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Create a metric view workspace.gold.acquisition_metrics on workspace.gold.acquisition_monthly, and run it.
# MAGIC
# MAGIC Dimensions: Month, Acquisition Channel.
# MAGIC Measures:
# MAGIC - Marketing Spend = SUM(spend_aed); Leads = SUM(leads); Signups = SUM(signups)
# MAGIC - CAC = Marketing Spend / Signups; Cost per Lead = Marketing Spend / Leads
# MAGIC - Activation Rate = SUM(activated_signups) / Signups
# MAGIC - Churned Share = SUM(churned_to_date) / Signups
# MAGIC - Revenue to Date = SUM(revenue_to_date_aed)
# MAGIC - Return on Spend = Revenue to Date / Marketing Spend
# MAGIC Synonyms: Return on Spend -&gt; payback, ROAS, LTV to CAC; CAC -&gt; customer acquisition cost; Marketing Spend -&gt; spend, ad spend.</pre></div>

# COMMAND ----------

# MAGIC %md
# MAGIC **Check:** Paid Social has the biggest spend and the cheapest leads, but one of the lowest returns on spend.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT `Acquisition Channel`, MEASURE(`Marketing Spend`) AS spend_aed, MEASURE(`Cost per Lead`) AS cost_per_lead,
# MAGIC        MEASURE(`CAC`) AS cac, MEASURE(`Churned Share`) AS churned_share, MEASURE(`Return on Spend`) AS return_on_spend
# MAGIC FROM workspace.gold.acquisition_metrics
# MAGIC GROUP BY ALL ORDER BY spend_aed DESC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-steps { display: flex; flex-direction: column; gap: 20px; }
# MAGIC .ds-step { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 18px 20px; border-top: 6px solid var(--accent, #4299E0); }
# MAGIC .ds-step.blue { --accent:#4299E0; --tint:rgba(66,153,224,0.10); }
# MAGIC .ds-step.green { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-step.amber { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-step.coral { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-step.red { --accent:#98102A; --tint:rgba(152,16,42,0.10); }
# MAGIC .ds-step.teal { --accent:#1B5162; --tint:rgba(27,81,98,0.10); }
# MAGIC .ds-step-head { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
# MAGIC .ds-step-num { width: 36px; height: 36px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 18pt; font-weight: 800; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-step-title { font-size: 18pt; font-weight: 700; color: #0b2026; }
# MAGIC .ds-step-text { font-size: 14pt; color: #0b2026; line-height: 1.6; }
# MAGIC .ds-step-text ul { margin: 0; padding-left: 20px; }
# MAGIC .ds-step-text li { margin-bottom: 8px; }
# MAGIC .ds-example { margin-top: 12px; padding: 10px 12px; border-radius: 8px; font-size: 14pt; line-height: 1.5; background: var(--tint); border-left: 4px solid var(--accent); }
# MAGIC .ds-example ul { margin: 4px 0 0; padding-left: 18px; }
# MAGIC .ds-example li { margin-bottom: 4px; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 3</div><div class="mh-title">Build your Genie Agent</div><div class="mh-sub">A natural-language analyst over the gold layer, that the founders would actually trust</div></div>
# MAGIC <div class="ds-steps"><div class="ds-step blue"><div class="ds-step-head"><div class="ds-step-num">1</div><div class="ds-step-title">New → Genie Agent</div></div><div class="ds-step-text"><div>Called Genie space in older screens. Name it <code>Falak Business Analyst</code>.</div></div></div><div class="ds-step green"><div class="ds-step-head"><div class="ds-step-num">2</div><div class="ds-step-title">Add 4 data sources</div></div><div class="ds-step-text"><ul><li><code>workspace.gold.revenue_metrics</code> (metric view)</li><li><code>workspace.gold.acquisition_metrics</code> (metric view)</li><li><code>workspace.gold.customer_360</code></li><li><code>workspace.gold.support_tickets</code></li></ul></div></div><div class="ds-step amber"><div class="ds-step-head"><div class="ds-step-num">3</div><div class="ds-step-title">Warehouse</div></div><div class="ds-step-text"><div>The default <strong>Serverless Starter Warehouse</strong>.</div></div></div><div class="ds-step coral"><div class="ds-step-head"><div class="ds-step-num">4</div><div class="ds-step-title">Paste the description, instructions and sample questions below</div></div><div class="ds-step-text"><div>In <strong>Settings</strong> (description) and <strong>Instructions</strong> (text instructions, sample questions).</div></div></div></div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 3.1</div><div class="mh-title">Teach it the business</div><div class="mh-sub">Copy each block into the matching field: description in Settings, the rest in Instructions</div></div>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Description</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Ask anything about Falak's business: revenue and MRR, churn and at-risk accounts, marketing efficiency by channel, and support tickets. Data is up to the end of October 2026, money in AED.</pre></div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Instructions</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">You are Falak's business analyst. Falak sells invoicing and payment-link software to SMEs in the GCC.
# MAGIC - Money is in AED. Round to whole AED and use thousands separators.
# MAGIC - "Today" is the as_of_date column in customer_360 (end of October 2026). "Last month" = October 2026.
# MAGIC - MRR is a monthly snapshot: always filter or group revenue_metrics by Month. Never sum MRR across months.
# MAGIC - "Churn rate" means the Logo Churn Rate measure, per month. "Customers" means active paying customers.
# MAGIC - "At risk" means customer_360.risk_level = 'high' and status = 'active'. Show risk_reasons when listing them.
# MAGIC - For questions about marketing efficiency, CAC, payback or LTV, use acquisition_metrics. Return on Spend below 1.3 is poor.
# MAGIC - KSA = Saudi Arabia. UAE = United Arab Emirates.
# MAGIC - When you list customers, show company_name, country, plan_name, mrr_aed and account_manager.
# MAGIC - For "what happened" questions about a period or a country, investigate like an analyst: compare churned customers, failed invoices (customer_360) and support ticket topics (support_tickets) with the months before, not only MRR.</pre></div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Sample questions (one per line)</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">What is our MRR trend over the last 12 months?
# MAGIC Which accounts are at risk right now and how much MRR is at stake?
# MAGIC Which acquisition channel gives the best return on marketing spend?
# MAGIC What happened in Saudi Arabia in summer 2026?
# MAGIC Do customers who connect an integration early churn less?</pre></div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-table { width: 100%; border-collapse: collapse; font-size: 14pt; background: #F9F7F4; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .ds-table th { text-align: left; background: #1B5162; color: #FFFFFF; font-weight: 700; padding: 10px 12px; }
# MAGIC .ds-table td { padding: 9px 12px; border-bottom: 1px solid #EEEDE9; vertical-align: top; line-height: 1.45; }
# MAGIC .ds-table tr:nth-child(even) td { background: #FFFFFF; }
# MAGIC .ds-table td.k { font-weight: 700; white-space: nowrap; }
# MAGIC .ds-table td.mono, .ds-table span.mono { font-family: Menlo, Consolas, monospace; font-size: 14pt; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 3.2</div><div class="mh-title">5 prompts to try</div><div class="mh-sub">Validated on the Falak data. Each one uncovers a story the founders did not see.</div></div>
# MAGIC <table class="ds-table"><thead><tr><th>#</th><th>The story</th><th>What Genie found in our test</th></tr></thead><tbody><tr><td class="k">1</td><td>Who we might lose next</td><td>Rimal Logistics Co. (Riyadh, Scale, ~5,000 AED MRR) at the top: usage down 60-70%, 2 failed invoices, a cancellation ticket. Then four Scale accounts with usage down 50%+</td></tr><tr><td class="k">2</td><td>Growth at any cost</td><td>Paid Social: 7.6M AED spent, ~5,400 AED CAC, return on spend only ~1.1-1.2x, below the 1.3 threshold</td></tr><tr><td class="k">3</td><td>The KSA incident</td><td>MRR grew until July, then in August churn jumped to 80 customers, net new MRR turned negative, and payment-failure tickets dominated support (344 over the summer)</td></tr><tr><td class="k">4</td><td>The activation lever</td><td>~14% churn for customers who connected an integration in their first 14 days vs ~43% for the rest: 3x less</td></tr><tr><td class="k">5</td><td>A product opportunity</td><td>e-invoicing is the #1 UAE support topic since March 2026 (~500 tickets), ahead of how-to and billing questions</td></tr></tbody></table>
# MAGIC </div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt 1 · Who we might lose next</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Who are our 5 biggest at-risk accounts, and why are they at risk?</pre></div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt 2 · Growth at any cost</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Where are we wasting the most marketing money?</pre></div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt 3 · The KSA incident</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">What happened in Saudi Arabia in summer 2026?</pre></div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt 4 · The activation lever</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">Do customers who connect an integration in their first 14 days churn less? Compare the churn rate of both groups.</pre></div>
# MAGIC <div style="background: #F9F7F4; border: 2px solid #EEEDE9; border-radius: 8px; margin: 12px auto; font-family: sans-serif; max-width: 1100px; overflow: hidden;"><div style="display: flex; justify-content: space-between; align-items: center; background: #EEEDE9; padding: 10px 16px; border-bottom: 1px solid #DCE0E2;"><span style="font-size: 14pt; font-weight: 700; color: #0b2026; letter-spacing: 1px; text-transform: uppercase;">Prompt 5 · A product opportunity</span><button onclick="var pre=this.parentElement.nextElementSibling; var ta=document.createElement('textarea'); ta.value=pre.innerText; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); var b=this; b.innerText='\u2713 Copied!'; setTimeout(function(){b.innerText='Copy';},2000);" style="background: #FF5F46; color: #FFFFFF; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14pt; font-weight: 700; cursor: pointer; white-space: nowrap;">Copy</button></div><pre style="margin: 0; padding: 16px 18px; background: #FFFFFF; color: #0b2026; font-family: Menlo, Consolas, monospace; font-size: 14pt; line-height: 1.55; white-space: pre-wrap; word-wrap: break-word; overflow-x: auto;">What are UAE customers asking support about since March 2026, and what does it tell us about the product?</pre></div>

# COMMAND ----------

# MAGIC %md
# MAGIC **Answer not right?** Improve the instructions, or add an example SQL query in **Instructions → SQL queries**, then ask again. Without the last instruction line ("investigate like an analyst"), prompt 3 only looks at MRR and misses the incident: a good example of how much instructions matter.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; display: flex; flex-direction: column; gap: 22px; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .mh { text-align: left; }
# MAGIC .mh-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #FF5F46; margin-bottom: 4px; }
# MAGIC .mh-title { font-size: 21pt; font-weight: 700; margin-bottom: 4px; color: #0b2026; line-height: 1.25; }
# MAGIC .mh-sub { font-size: 15pt; color: #5E7077; line-height: 1.5; }
# MAGIC code { background: #EEEDE9; padding: 1px 6px; border-radius: 4px; font-size: 14pt; color: #0b2026; }
# MAGIC
# MAGIC .ds-callout { border-left: 6px solid var(--accent, #1B5162); border-radius: 8px; padding: 18px 24px; background: var(--tint, #F8F9FC); box-shadow: 0 2px 8px rgba(27,49,57,0.06); font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-eyebrow { font-size: 14pt; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--accent, #1B5162); margin-bottom: 6px; }
# MAGIC .ds-callout ul { margin: 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-callout li { margin-bottom: 10px; } .ds-callout li:last-child { margin-bottom: 0; }
# MAGIC .ds-callout.info { --accent:#1B5162; --tint:#F8F9FC; }
# MAGIC .ds-callout.caution { --accent:#FFAB00; --tint:rgba(255,171,0,0.12); }
# MAGIC .ds-callout.danger { --accent:#FF5F46; --tint:rgba(255,95,70,0.10); }
# MAGIC .ds-callout.success { --accent:#00A972; --tint:rgba(0,169,114,0.10); }
# MAGIC .ds-callout.row { display: flex; align-items: center; gap: 16px; }
# MAGIC .ds-callout-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent); color: #fff; font-size: 22pt; font-weight: 700; line-height: 1; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
# MAGIC .ds-callout.caution .ds-callout-icon { color: #0b2026; }
# MAGIC .ds-callout-title { font-size: 16pt; font-weight: 700; color: #0b2026; margin-bottom: 10px; line-height: 1.3; }
# MAGIC
# MAGIC .ds-band-solid { background: #1B5162; color: #fff; border-radius: 10px; padding: 22px 28px; text-align: center; border-top: 6px solid var(--accent, #FF5F46); box-shadow: 0 2px 10px rgba(27,49,57,0.12); }
# MAGIC .ds-band-lead { font-size: 17pt; font-weight: 700; color: #fff; line-height: 1.3; margin-bottom: 8px; }
# MAGIC .ds-band-sub { font-size: 14pt; color: #F9F7F4; font-weight: 600; line-height: 1.4; }
# MAGIC .ds-band-bordered { background: #F8F9FC; border: 3px solid #1B5162; border-radius: 8px; padding: 16px 24px; text-align: center; font-size: 16pt; color: #0b2026; line-height: 1.5; }
# MAGIC </style>
# MAGIC <div class="mh"><div class="mh-eyebrow">Step 3.3</div><div class="mh-title">Plug it into your app</div><div class="mh-sub">Copy the Genie Agent ID: open the agent → About, or take it from the URL <code>.../genie/rooms/&lt;ID&gt;</code></div></div>
# MAGIC <div class="ds-callout success"><div class="ds-eyebrow">Then, in Claude Code</div><div class="ds-callout-title">Open guides/4_App_with_Claude.md on your laptop</div><div>Tell Claude: <em>"Connect to my app (profile hackathon). Add the Overview page from examples, connect my Genie Agent &lt;ID&gt; and add the Ask Genie page. Deploy."</em> Then spend the rest of the time on your own idea.</div></div>
# MAGIC <div class="ds-band-solid" style="--accent:#FF5F46;"><div class="ds-band-lead">Demo: the problem in one sentence, one live Genie question, one app feature, what you would build next week.</div></div>
# MAGIC </div>
