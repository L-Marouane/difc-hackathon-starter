import {
  useAnalyticsQuery,
  DataTable,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Skeleton,
} from '@databricks/appkit-ui/react';
import { z } from 'zod';

const TableRow = z.object({ layer: z.string() });

const LAYERS = [
  { key: 'bronze', title: 'Bronze', hint: 'raw data, as delivered' },
  { key: 'silver', title: 'Silver', hint: 'cleaned and deduplicated' },
  { key: 'gold', title: 'Gold', hint: 'business-ready, feeds this app' },
];

const NEXT_STEPS = [
  'Build bronze, silver and gold with Genie Code (01_Hackathon_Guide, step 1). Watch the counters above fill up.',
  'Define your metrics once with metric views (step 2).',
  'Create your Genie Agent (step 3).',
  'Open Claude Code in the app/ folder and ask: "Add the Overview page from examples and connect my Genie Agent <id>".',
];

function LayerCounters() {
  const { data, loading, error } = useAnalyticsQuery('lakehouse_tables', {});

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {LAYERS.map((l) => (
          <Skeleton key={l.key} className="h-28" />
        ))}
      </div>
    );
  }
  if (error) {
    return (
      <div className="text-destructive bg-destructive/10 p-3 rounded-md text-sm">
        Could not read the lakehouse: {error}
      </div>
    );
  }
  const rows = (Array.isArray(data) ? data : []).map((r) => TableRow.safeParse(r)).filter((r) => r.success);
  const count = (layer: string) => rows.filter((r) => r.data.layer === layer).length;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {LAYERS.map((l) => (
        <Card key={l.key}>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">{l.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">{count(l.key)}</div>
            <div className="text-xs text-muted-foreground mt-1">tables · {l.hint}</div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export function HomePage() {
  return (
    <div className="space-y-6 w-full max-w-6xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-foreground">Welcome to Falak</h2>
        <p className="text-sm text-muted-foreground mt-1">
          This app is live and connected to your lakehouse. Build the data, then make the app yours with Claude Code.
        </p>
      </div>

      <LayerCounters />

      <Card>
        <CardHeader>
          <CardTitle>Next steps</CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="list-decimal list-inside space-y-2 text-sm text-foreground">
            {NEXT_STEPS.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ol>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your lakehouse tables</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable
            queryKey="lakehouse_tables"
            parameters={{}}
            filterColumn="table_name"
            filterPlaceholder="Search tables..."
            pageSize={10}
          />
        </CardContent>
      </Card>
    </div>
  );
}
