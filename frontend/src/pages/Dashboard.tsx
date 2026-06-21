import { useEffect, useState } from 'react';
import { apiGet, getList } from '../api/client';
import { Card } from '../components/Card';
import { KpiCard } from '../components/KpiCard';
import type { AppProfile, DashboardSummary } from '../types';

export function Dashboard() {
  const [apps, setApps] = useState<AppProfile[]>([]);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    getList<AppProfile>('/apps/').then((items) => {
      setApps(items);
      if (items[0]) apiGet<DashboardSummary>(`/dashboard/summary/?app=${items[0].id}`).then(setSummary);
    });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Growth Dashboard</h1>
        <p className="mt-2 text-slate-600">Track, diagnose, recommend, and log manual actions. No external changes are executed.</p>
      </div>

      {!summary && (
        <Card title="Getting started">
          <p className="text-slate-600">Seed demo data or create an app profile to begin.</p>
          <code className="mt-3 block rounded-xl bg-slate-100 p-3 text-sm">python manage.py seed_demo</code>
        </Card>
      )}

      {summary && (
        <>
          <div className="grid grid-cols-5 gap-4">
            <KpiCard label="Installs" value={summary.kpis.installs} />
            <KpiCard label="Visitors" value={summary.kpis.store_visitors} />
            <KpiCard label="Conversion" value={`${summary.kpis.conversion_rate}%`} />
            <KpiCard label="D1 retention" value={`${summary.kpis.day_1_retention}%`} />
            <KpiCard label="D7 retention" value={`${summary.kpis.day_7_retention}%`} />
          </div>

          <Card title="Current bottleneck">
            <div className="rounded-xl bg-amber-50 p-4">
              <p className="font-semibold text-amber-900">{summary.bottleneck}</p>
              <ul className="mt-2 list-disc pl-5 text-sm text-amber-900">
                {summary.evidence.map((item) => <li key={item}>{item}</li>)}
              </ul>
            </div>
          </Card>

          <Card title="Top recommendations">
            <div className="space-y-3">
              {summary.top_recommendations.length === 0 && <p className="text-slate-600">Generate a growth report to create recommendations.</p>}
              {summary.top_recommendations.map((rec) => (
                <div key={rec.id} className="rounded-xl border border-slate-200 p-4">
                  <p className="font-semibold">{rec.title}</p>
                  <p className="mt-1 text-sm text-slate-600">{rec.suggested_human_action}</p>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
