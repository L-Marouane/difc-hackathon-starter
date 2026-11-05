// Small helpers shared by the scripts: CLI calls and .env read/write.
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';

export const readEnv = () =>
  existsSync('.env')
    ? Object.fromEntries(
        readFileSync('.env', 'utf8')
          .split('\n')
          .filter((l) => l.includes('='))
          .map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1)])
      )
    : {};

export const writeEnv = (vars) =>
  writeFileSync(
    '.env',
    Object.entries(vars)
      .map(([k, v]) => `${k}=${v}`)
      .join('\n') + '\n'
  );

export const cli = (profile) => ({
  run: (...a) => execFileSync('databricks', [...a, '--profile', profile], { stdio: 'inherit' }),
  json: (...a) =>
    JSON.parse(execFileSync('databricks', [...a, '--profile', profile, '-o', 'json'], { encoding: 'utf8' })),
});

export const args = () =>
  Object.fromEntries(
    process.argv
      .slice(2)
      .reduce((acc, a, i, all) => (a.startsWith('--') ? [...acc, [a.slice(2), all[i + 1]]] : acc), [])
  );
