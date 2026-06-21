import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import { formatDateTime, formatNumber, formatPercent, statusTone } from '../lib/format';
import type { Recommendation } from '../types';

export function Recommendations() {
  const { selectedApp } = useAppContext();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [message, setMessage] = useState('');

  const refresh = async () => {
    if (!selectedApp) return;
    const items = await apiGet<{ results: Recommendation[] } | Recommendation[]>(`/recommendations/?app=${selectedApp.id}`);
    setRecommendations(Array.isArray(items) ? items : items.results);
  };

  useEffect(() => {
    refresh().catch(() => setRecommendations([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedApp, message]);

  const updateStatus = async (id: number, action: 'accept' | 'reject' | 'done' | 'monitoring') => {
    setMessage('');
    await apiPost(`/recommendations/${id}/${action}/`, {});
    setMessage(`Recommendation marked as ${action}.`);
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Recommendation queue</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Track human decisions, not automation</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
          Accepted means “the developer will do this manually.” It does not trigger any write operation in Play Console or ads.
        </p>
      </div>

      {!selectedApp && <Card title="No app selected"><p className="text-sm text-slate-600">Choose an app profile first.</p></Card>}

      {selectedApp && (
        <div className="space-y-4">
          {message && <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700">{message}</div>}
          <Card title="Queue overview">
            <div className="grid gap-3 md:grid-cols-4">
              {['new', 'accepted', 'done', 'monitoring'].map((status) => {
                const count = recommendations.filter((item) => item.status === status).length;
                return (
                  <div key={status} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="text-xs uppercase tracking-[0.22em] text-slate-500">{status}</p>
                    <p className="mt-2 text-3xl font-semibold text-slate-950">{formatNumber(count)}</p>
                  </div>
                );
              })}
            </div>
          </Card>

          <div className="grid gap-4 xl:grid-cols-2">
            {recommendations.map((rec) => (
              <Card key={rec.id} title={rec.title}>
                <div className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    <span className="rounded-full border border-slate-200 bg-slate-100 px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] text-slate-600">
                      {rec.category}
                    </span>
                    <span className={`rounded-full border px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] ${statusTone(rec.priority)}`}>
                      {rec.priority}
                    </span>
                    <span className={`rounded-full border px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] ${statusTone(rec.status)}`}>
                      {rec.status}
                    </span>
                    <span className="rounded-full border border-slate-200 bg-white px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] text-slate-500">
                      {formatPercent(rec.confidence_score)}
                    </span>
                  </div>
                  <p className="text-sm leading-6 text-slate-600">{rec.suggested_human_action}</p>
                  <p className="text-sm leading-6 text-slate-600">
                    Why it matters: <span className="font-medium text-slate-900">{rec.why_this_matters}</span>
                  </p>
                  <p className="text-sm leading-6 text-slate-600">
                    Watch: <span className="font-medium text-slate-900">{rec.watch_metric}</span>
                  </p>
                  <p className="text-xs text-slate-500">Updated {formatDateTime(rec.updated_at || undefined)}</p>
                  <div className="flex flex-wrap gap-2">
                    <button type="button" onClick={() => updateStatus(rec.id, 'accept')} className="rounded-full bg-slate-950 px-4 py-2 text-sm font-semibold text-white">
                      Accept
                    </button>
                    <button type="button" onClick={() => updateStatus(rec.id, 'reject')} className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-800">
                      Reject
                    </button>
                    <button type="button" onClick={() => updateStatus(rec.id, 'done')} className="rounded-full border border-emerald-300 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-800">
                      Done
                    </button>
                    <button type="button" onClick={() => updateStatus(rec.id, 'monitoring')} className="rounded-full border border-amber-300 bg-amber-50 px-4 py-2 text-sm font-semibold text-amber-800">
                      Monitoring
                    </button>
                  </div>
                </div>
              </Card>
            ))}
            {recommendations.length === 0 && (
              <Card title="No recommendations yet">
                <p className="text-sm text-slate-600">Generate a growth report to populate the queue.</p>
              </Card>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
