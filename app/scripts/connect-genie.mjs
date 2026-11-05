#!/usr/bin/env node
// Give the app access to your Genie Agent and expose its ID as DATABRICKS_GENIE_SPACE_ID.
// Then add genie() to server/server.ts and the Genie page (see examples/README.md), and deploy.
// Usage: node scripts/connect-genie.mjs --space <genie-agent-id>
import { readFileSync, writeFileSync } from 'node:fs';
import { args, cli, readEnv, writeEnv } from './lib.mjs';

const space = args().space;
const env = readEnv();
if (!space || !env.DATABRICKS_CONFIG_PROFILE) {
  console.error('Usage: node scripts/connect-genie.mjs --space <genie-agent-id>   (after configure.mjs)');
  process.exit(1);
}
const { json } = cli(env.DATABRICKS_CONFIG_PROFILE);
const appName = env.DATABRICKS_APP_NAME;
const app = json('apps', 'get', appName);

const resources = (app.resources ?? []).filter((r) => !r.genie_space);
resources.push({ name: 'genie-space', genie_space: { name: 'falak-genie', space_id: space, permission: 'CAN_RUN' } });
const scopes = [...new Set([...(app.user_api_scopes ?? []), 'dashboards.genie'])];
json(
  'api',
  'patch',
  `/api/2.0/apps/${appName}`,
  '--json',
  JSON.stringify({ name: appName, resources, user_api_scopes: scopes })
);

const yaml = readFileSync('app.yaml', 'utf8');
if (!yaml.includes('DATABRICKS_GENIE_SPACE_ID')) {
  writeFileSync('app.yaml', yaml.trimEnd() + '\n  - name: DATABRICKS_GENIE_SPACE_ID\n    valueFrom: genie-space\n');
}
writeEnv({ ...env, DATABRICKS_GENIE_SPACE_ID: space });
console.log(
  `Genie Agent ${space} attached to ${appName}. Next: add genie() in server/server.ts and the Genie page, then npm run deploy:app`
);
