import { FormEvent, useEffect, useState } from 'react';
import { apiGet, apiPost } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import { formatDate } from '../lib/format';
import type { GrowthReport } from '../types';

export function Reports() {
  const { selectedApp } = useAppContext();
  const [reports, setReports] = useState<GrowthReport[]>([]);
  const [message, setMessage] = useState('');
  const [periodStart, setPeriodStart] = useState('');
  const [periodEnd, setPeriodEnd] = useState('');

  const refresh = async () => {
    if (!selectedApp) return;
    const items = await apiGet<{ results: GrowthReport[] } | GrowthReport[]>(`/growth-reports/?app=${selectedApp.id}`);
    setReports(Array.isArray(items) ? items : items.results);
  };

  useEffect(() => {
    refresh().catch(() => setReports([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedApp]);

  const generate = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedApp) return;
    setMessage('');
    try {
      await apiPost<GrowthReport>('/growth-reports/generate/', {
        app: selectedApp.id,
        report_type: 'weekly',
        period_start: periodStart || undefined,
        period_end: periodEnd || undefined,
      });
      setMessage('Report generated.');
      await refresh();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Unable to generate report');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Growth reports</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Daily and weekly report snapshots</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
          Reports summarize the diagnosis, evidence, and the next manual action. They are conservative by design.
        </p>
      </div>

      {!selectedApp && <Card title="No app selected"><p className="text-sm text-slate-600">Select an app profile to view reports.</p></Card>}

      {selectedApp && (
        <div className="grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
          <Card title="Generate report">
            <form className="space-y-4" onSubmit={generate}>
              <label className="block">
                <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-slate-500">Period start</span>
                <input type="date" value={periodStart} onChange={(event) => setPeriodStart(event.target.value)} className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              </label>
              <label className="block">
                <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-slate-500">Period end</span>
                <input type="date" value={periodEnd} onChange={(event) => setPeriodEnd(event.target.value)} className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              </label>
              <button type="submit" className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white">Generate weekly report</button>
            </form>
            {message && <p className="mt-4 text-sm text-slate-600">{message}</p>}
          </Card>

          <Card title="Recent reports">
            <div className="space-y-3">
              {reports.length === 0 && <p className="text-sm text-slate-600">No reports yet.</p>}
              {reports.map((report) => (
                <article key={report.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-[0.22em] text-slate-500">
                    {report.report_type} · {formatDate(report.period_start)} to {formatDate(report.period_end)}
                  </p>
                  <p className="mt-2 font-semibold text-slate-900">{report.bottleneck || 'No bottleneck set'}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{report.summary}</p>
                  <p className="mt-2 text-xs text-slate-500">Provider: {report.ai_provider}</p>
                </article>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
