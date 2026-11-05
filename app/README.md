# Falak Founder Console (AppKit app)

Deployed for you by `00_Setup_Data` as `falak-app`. Almost empty on purpose: a home page showing your lakehouse tables per layer, wired to your SQL warehouse. Build the rest with Claude Code ([CLAUDE.md](CLAUDE.md)).

```bash
npm install
node scripts/configure.mjs --profile <your-cli-profile>   # connects this folder to the deployed app, writes .env
npm run dev                                               # local preview on http://localhost:8000
npm run deploy:app                                        # check, upload and deploy (about 2 minutes)
node scripts/connect-genie.mjs --space <genie-agent-id>   # attach your Genie Agent to the app
```

| Path | What |
|---|---|
| `client/src/pages/home/HomePage.tsx` | Starter home page |
| `client/src/App.tsx` | Layout and routes |
| `config/queries/*.sql` | SQL queries (file name = `queryKey`) |
| `server/server.ts` | AppKit plugins and custom routes |
| `examples/` | Tested Overview and Ask Genie pages to drop in |
| `app.yaml` | Start command and environment (warehouse, Genie) |
