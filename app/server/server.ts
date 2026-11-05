import { createApp, analytics, server } from '@databricks/appkit';

// Add plugins here as the app grows, e.g. genie() once a Genie Agent is connected
// (see examples/README.md and scripts/connect-genie.mjs).
createApp({
  plugins: [analytics(), server()],
}).catch(console.error);
