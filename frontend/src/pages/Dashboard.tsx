import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../api/client';
import { Card } from '../components/Card';
import { KpiCard } from '../components/KpiCard';
import { useAppContext } from '../context/AppContext';
import type { DashboardSummary, GrowthReport } from '../types';
import { formatDate, formatDateTime, formatNumber, formatPercent, statusTone } from '../lib/format';

export function Dashboard() {
  const { selectedApp } = useAppContext();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!selectedApp) return;
    apiGet<DashboardSummary>(`/dashboard/summary/?app=${selectedApp.id}`)
      .then(setSummary)
      .catch((err: Error) => setError(err.message));
  }, [selectedApp]);

  const generateReport = async () => {
    if (!selectedApp) return;
    setIsGenerating(true);
    setError('');
    try {
      const today = new Date().toISOString().slice(0, 10);
      const report = await apiPost<GrowthReport>('/growth-reports/generate/', {
        app: selectedApp.id,
        report_type: 'weekly',
        period_end: today,
      });
      const updated = await apiGet<DashboardSummary>(`/dashboard/summary/?app=${selectedApp.id}`);
      setSummary({ ...updated, latest_report: report });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to generate report');
    } finally {
      setIsGenerating(false);
    }
  };

  const nextAction = summary?.next_recommendation ?? summary?.top_recommendations?.[0] ?? null;

  return (
    <div className="space-y-6">
      <section className="rounded-[1.75rem] border border-slate-200 bg-slate-950 px-6 py-6 text-white shadow-[0_30px_100px_rgba(15,23,42,0.18)]">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.32em] text-amber-300/80">Dashboard</p>
            <h1 className="mt-3 text-4xl font-semibold tracking-tight">Growth bottlenecks, manual actions, and outcome tracking</h1>
            <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-300">
              The copilot diagnoses the bottleneck and suggests the next human step. It does not publish changes, spend budget, or write to Play Console.
            </p>
          </div>
          <button
            type="button"
            onClick={generateReport}
            disabled={!selectedApp || isGenerating}
            className="inline-flex items-center justify-center rounded-full bg-amber-300 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-amber-200 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isGenerating ? 'Generating report...' : 'Generate weekly report'}
          </button>
        </div>
        {selectedApp && (
          <div className="mt-6 grid gap-3 text-sm text-slate-200 md:grid-cols-3">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-400">App</p>
              <p className="mt-2 font-medium text-white">{selectedApp.name}</p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Package</p>
              <p className="mt-2 font-medium text-white">{selectedApp.package_name}</p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Latest report</p>
              <p className="mt-2 font-medium text-white">{summary?.latest_report ? formatDate(summary.latest_report.report_date) : 'No report yet'}</p>
            </div>
          </div>
        )}
      </section>

      {error && <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">{error}</div>}

      {!selectedApp && (
        <Card title="No app profile selected">
          <p className="text-sm leading-6 text-slate-600">Create or select an app profile to see the dashboard.</p>
        </Card>
      )}

      {summary && selectedApp && (
        <>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <KpiCard label="Installs" value={formatNumber(summary.kpis.installs)} hint={`${formatDate(summary.window.start)} to ${formatDate(summary.window.end)}`} />
            <KpiCard label="Visitors" value={formatNumber(summary.kpis.store_visitors)} hint="Store visitors in the selected window" />
            <KpiCard label="Conversion" value={formatPercent(summary.kpis.conversion_rate)} hint="Average listing conversion rate" />
            <KpiCard label="Retention" value={`${formatPercent(summary.kpis.day_1_retention)} / ${formatPercent(summary.kpis.day_7_retention)}`} hint="D1 / D7 retention" />
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <KpiCard label="Reviews" value={formatNumber(summary.kpis.reviews)} hint={`Average rating ${summary.kpis.rating.toFixed(1)}`} />
            <KpiCard label="Crashes" value={summary.kpis.crashes.toFixed(2)} hint="Average crash rate in the window" />
            <KpiCard label="ANRs" value={summary.kpis.anrs.toFixed(2)} hint="Average ANR rate in the window" />
            <KpiCard label="Ads spend" value={`$${summary.kpis.ads_spend.toFixed(2)}`} hint={`CPI $${summary.kpis.cpi.toFixed(2)}`} />
          </div>

          <div className="grid gap-4 xl:grid-cols-[1.6fr_1fr]">
            <Card title="Main bottleneck diagnosis">
              <div className="space-y-4">
                <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-100 px-3 py-1 text-xs font-medium uppercase tracking-[0.24em] text-slate-600">
                  <span>{summary.bottleneck}</span>
                  <span className="rounded-full bg-white px-2 py-1 normal-case tracking-normal text-slate-500">{summary.confidence_score.toFixed(2)}</span>
                </div>
                <ul className="space-y-2 text-sm leading-6 text-slate-700">
                  {summary.evidence.map((item) => (
                    <li key={item} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
                <p className="text-sm text-slate-600">
                  Watch metric: <span className="font-medium text-slate-900">{summary.watch_metric}</span>
                </p>
              </div>
            </Card>

            <Card title="Next recommended action">
              {nextAction ? (
                <div className="space-y-4">
                  <div className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] ${statusTone(nextAction.priority)}`}>
                    {nextAction.priority} priority
                  </div>
                  <p className="text-lg font-semibold text-slate-900">{nextAction.title}</p>
                  <p className="text-sm leading-6 text-slate-600">{nextAction.suggested_human_action}</p>
                  <p className="text-sm leading-6 text-slate-600">
                    Why this matters: <span className="font-medium text-slate-900">{nextAction.why_this_matters}</span>
                  </p>
                  <p className="text-sm leading-6 text-slate-600">
                    Metric to watch: <span className="font-medium text-slate-900">{nextAction.watch_metric}</span>
                  </p>
                </div>
              ) : (
                <p className="text-sm text-slate-600">Generate a report to create the next action.</p>
              )}
            </Card>
          </div>

          <div className="grid gap-4 xl:grid-cols-2">
            <Card title="Top recommendations">
              <div className="space-y-3">
                {summary.top_recommendations.length === 0 && <p className="text-sm text-slate-600">No recommendations yet.</p>}
                {summary.top_recommendations.map((rec) => (
                  <article key={rec.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-slate-200 bg-white px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] text-slate-600">
                        {rec.category}
                      </span>
                      <span className={`rounded-full border px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] ${statusTone(rec.priority)}`}>
                        {rec.priority}
                      </span>
                      <span className={`rounded-full border px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] ${statusTone(rec.status)}`}>
                        {rec.status}
                      </span>
                    </div>
                    <p className="mt-3 font-semibold text-slate-900">{rec.title}</p>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{rec.suggested_human_action}</p>
                  </article>
                ))}
              </div>
            </Card>

            <Card title="Recent manual actions">
              <div className="space-y-3">
                {summary.recent_actions.length === 0 && <p className="text-sm text-slate-600">No manual actions logged yet.</p>}
                {summary.recent_actions.map((action) => (
                  <article key={action.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-500">{formatDate(action.action_date)}</p>
                    <p className="mt-2 font-semibold text-slate-900">{action.title}</p>
                    <p className="mt-2 text-sm leading-6 text-slate-600">{action.description || 'No description entered.'}</p>
                    <p className="mt-2 text-xs text-slate-500">Observed result: {action.outcome_notes || 'Pending'}</p>
                  </article>
                ))}
              </div>
            </Card>
          </div>

          <div className="grid gap-4 xl:grid-cols-2">
            <Card title="Review themes">
              <div className="space-y-3">
                {summary.review_themes.length === 0 && <p className="text-sm text-slate-600">Run review analysis to extract themes.</p>}
                {summary.review_themes.map((theme) => (
                  <article key={theme.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="font-semibold text-slate-900">{theme.theme}</p>
                      <span className={`rounded-full border px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] ${statusTone(theme.severity)}`}>
                        {theme.severity}
                      </span>
                    </div>
                    <p className="mt-2 text-sm text-slate-600">{theme.recommendation}</p>
                  </article>
                ))}
              </div>
            </Card>

            <Card title="Latest report snapshot">
              {summary.latest_report ? (
                <div className="space-y-3">
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-500">
                    {summary.latest_report.report_type} · {formatDate(summary.latest_report.report_date)}
                  </p>
                  <p className="text-sm leading-6 text-slate-700">{summary.latest_report.summary}</p>
                  <p className="text-sm text-slate-600">
                    Generated by <span className="font-medium text-slate-900">{summary.latest_report.ai_provider}</span>
                  </p>
                  <p className="text-sm text-slate-600">
                    Period: {formatDate(summary.latest_report.period_start)} to {formatDate(summary.latest_report.period_end)}
                  </p>
                </div>
              ) : (
                <p className="text-sm text-slate-600">No growth report has been generated yet.</p>
              )}
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
