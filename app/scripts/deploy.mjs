#!/usr/bin/env node
// Validate locally, push the source to the workspace and redeploy the app.
// Usage: npm run deploy:app   (after node scripts/configure.mjs)
import { execFileSync } from 'node:child_process';
import { cli, readEnv } from './lib.mjs';

const env = readEnv();
const profile = env.DATABRICKS_CONFIG_PROFILE;
if (!profile || !env.DATABRICKS_APP_SOURCE_PATH) {
  console.error('Run node scripts/configure.mjs --profile <cli-profile> first.');
  process.exit(1);
}
const { run, json } = cli(profile);
const app = env.DATABRICKS_APP_NAME;
const catalog = env.DATABRICKS_CATALOG ?? 'workspace';

// 1. Fail fast on this laptop: generate query types (checks every SQL file against the warehouse), typecheck, lint, build
execFileSync('npm', ['run', 'typegen', '--', '--wait'], { stdio: 'inherit' });
execFileSync('npm', ['run', 'typecheck'], { stdio: 'inherit' });
execFileSync('npm', ['run', 'lint'], { stdio: 'inherit' });
execFileSync('npm', ['run', 'build'], { stdio: 'inherit' });

// 2. The platform builds the app as its service principal, which must be able to read the tables (idempotent)
const sp = json('apps', 'get', app).service_principal_client_id;
for (const statement of [
  `GRANT USE CATALOG ON CATALOG ${catalog} TO \`${sp}\``,
  ...['bronze', 'silver', 'gold'].map((s) => `GRANT USE SCHEMA, SELECT ON SCHEMA ${catalog}.${s} TO \`${sp}\``),
]) {
  const res = json(
    'api',
    'post',
    '/api/2.0/sql/statements',
    '--json',
    JSON.stringify({ statement, warehouse_id: env.DATABRICKS_WAREHOUSE_ID, wait_timeout: '50s' })
  );
  if (res.status?.state !== 'SUCCEEDED') console.warn(`grant failed: ${statement}\n  ${JSON.stringify(res.status)}`);
}

// 3. Upload the source (sync honours .gitignore: no node_modules, dist or .env) and deploy
run('sync', '.', env.DATABRICKS_APP_SOURCE_PATH, '--full');
run('apps', 'deploy', app, '--source-code-path', env.DATABRICKS_APP_SOURCE_PATH);
console.log(`\nDeployed: ${json('apps', 'get', app).url}`);
