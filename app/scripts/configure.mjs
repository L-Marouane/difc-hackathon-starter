#!/usr/bin/env node
// Connect this folder to the app that 00_Setup_Data already deployed in your workspace.
// Usage: node scripts/configure.mjs --profile <cli-profile> [--app falak-app] [--catalog workspace]
import { args, cli, readEnv, writeEnv } from './lib.mjs';

const a = args();
const profile = a.profile ?? readEnv().DATABRICKS_CONFIG_PROFILE;
if (!profile) {
  console.error('Usage: node scripts/configure.mjs --profile <cli-profile> [--app falak-app] [--catalog workspace]');
  process.exit(1);
}
const { json } = cli(profile);
const appName = a.app ?? 'falak-app';

const auth = json('auth', 'describe');
if (auth.status !== 'success') {
  console.error(`Profile "${profile}" is not logged in. Run: databricks auth login --profile ${profile}`);
  process.exit(1);
}

let app;
try {
  app = json('apps', 'get', appName);
} catch {
  console.error(
    `App "${appName}" not found. Run the 00_Setup_Data notebook in your workspace first (it deploys the app).`
  );
  process.exit(1);
}
const warehouseId = (app.resources ?? []).find((r) => r.sql_warehouse)?.sql_warehouse.id;
const genieId = (app.resources ?? []).find((r) => r.genie_space)?.genie_space.space_id;
const sourcePath = app.active_deployment?.source_code_path ?? app.default_source_code_path;

writeEnv({
  ...readEnv(),
  DATABRICKS_CONFIG_PROFILE: profile,
  DATABRICKS_HOST: auth.details.host,
  DATABRICKS_APP_NAME: appName,
  DATABRICKS_APP_SOURCE_PATH: sourcePath,
  DATABRICKS_WAREHOUSE_ID: warehouseId,
  DATABRICKS_CATALOG: a.catalog ?? readEnv().DATABRICKS_CATALOG ?? 'workspace',
  ...(genieId ? { DATABRICKS_GENIE_SPACE_ID: genieId } : {}),
  DATABRICKS_APP_PORT: 8000,
});

console.log(`Connected to ${appName} on ${auth.details.host}
  url        ${app.url}
  source     ${sourcePath}
  warehouse  ${warehouseId}
  genie      ${genieId ?? '(not connected yet: node scripts/connect-genie.mjs --space <id>)'}
Next: npm run dev (local preview) or npm run deploy:app (deploy your changes)`);
