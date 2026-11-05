import {
  useAnalyticsQuery,
  BarChart,
  LineChart,
  DataTable,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Skeleton,
  Label,
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@databricks/appkit-ui/react';
import { sql } from '@databricks/appkit-ui/js';
import { useState } from 'react';
import { z } from 'zod';

const KpiRow = z.object({
  latest_month: z.string(),
  as_of_date: z.string().nullable(),
  mrr_aed: z.coerce.number(),
  mrr_growth_pct: z.coerce.number().nullable(),
  active_customers: z.coerce.number(),
  churned_customers: z.coerce.number(),
  high_risk_accounts: z.coerce.number(),
  mrr_at_risk_aed: z.coerce.number(),
});

const aed = (v: number) => `AED ${Math.round(v).toLocaleString('en-US')}`;

const COUNTRIES = ['United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Bahrain', 'Oman', 'Kuwait'];

function Kpi({ label, value, hint, tone }: { label: string; value: string; hint?: string; tone?: 'bad' | 'good' }) {
  const toneClass =
    tone === 'bad' ? 'text-destructive' : tone === 'good' ? 'text-emerald-600' : 'text-muted-foreground';
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-foreground">{value}</div>
        {hint && <div className={`text-xs mt-1 ${toneClass}`}>{hint}</div>}
      </CardContent>
    </Card>
  );
}

function KpiStrip() {
  const { data, loading, error } = useAnalyticsQuery('kpis', {});

  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Array.from({ length: 4 }, (_, i) => (
          <Skeleton key={i} className="h-28" />
        ))}
      </div>
    );
  }
  if (error) {
    return (
      <div className="text-destructive bg-destructive/10 p-3 rounded-md text-sm">
        Could not load KPIs: {error}. Did the pipeline build the gold tables?
      </div>
    );
  }
  const rows: unknown[] = Array.isArray(data) ? data : [];
  const parsed = KpiRow.safeParse(rows[0]);
  if (!parsed.success) return <div className="text-muted-foreground text-sm">No data yet.</div>;
  const k = parsed.data;
  const growth = k.mrr_growth_pct ?? 0;

  return (
    <div className="space-y-2">
      <p className="text-sm text-muted-foreground">
        {k.latest_month} · data as of {k.as_of_date}
      </p>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Kpi
          label="MRR"
          value={aed(k.mrr_aed)}
          hint={`${growth >= 0 ? '+' : ''}${growth}% vs previous month`}
          tone={growth >= 0 ? 'good' : 'bad'}
        />
        <Kpi
          label="Active customers"
          value={k.active_customers.toLocaleString('en-US')}
          hint={`${k.churned_customers} churned this month`}
        />
        <Kpi
          label="High-risk accounts"
          value={k.high_risk_accounts.toLocaleString('en-US')}
          hint="usage drop, failed payments or cancel intent"
          tone="bad"
        />
        <Kpi
          label="MRR at risk"
          value={aed(k.mrr_at_risk_aed)}
          hint={`${((100 * k.mrr_at_risk_aed) / Math.max(k.mrr_aed, 1)).toFixed(1)}% of MRR`}
          tone="bad"
        />
      </div>
    </div>
  );
}

export function OverviewPage() {
  const [country, setCountry] = useState<string>('all');

  return (
    <div className="space-y-6 w-full max-w-7xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-foreground">Overview</h2>
        <p className="text-sm text-muted-foreground mt-1">How Falak is doing, and who we might lose next.</p>
      </div>

      <KpiStrip />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="min-w-0">
          <CardHeader>
            <CardTitle>MRR (AED), last 18 months</CardTitle>
          </CardHeader>
          <CardContent>
            <LineChart queryKey="mrr_trend" parameters={{}} xKey="month" yKey="mrr_aed" smooth showSymbol={false} />
          </CardContent>
        </Card>
        <Card className="min-w-0">
          <CardHeader>
            <CardTitle>MRR gained vs lost (AED)</CardTitle>
          </CardHeader>
          <CardContent>
            <BarChart
              queryKey="mrr_trend"
              parameters={{}}
              xKey="month"
              yKey={['gained_mrr_aed', 'lost_mrr_aed']}
              colors={['#10b981', '#EB1600']}
              showLegend
            />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4 space-y-0">
          <CardTitle>At-risk accounts</CardTitle>
          <div className="flex items-center gap-2">
            <Label htmlFor="country" className="text-sm text-muted-foreground">
              Country
            </Label>
            <Select value={country} onValueChange={setCountry}>
              <SelectTrigger id="country" className="w-56">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All countries</SelectItem>
                {COUNTRIES.map((c) => (
                  <SelectItem key={c} value={c}>
                    {c}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          <DataTable
            queryKey="at_risk_accounts"
            parameters={{ country: sql.string(country) }}
            filterColumn="company_name"
            filterPlaceholder="Search accounts..."
            pageSize={10}
          />
        </CardContent>
      </Card>
    </div>
  );
}
