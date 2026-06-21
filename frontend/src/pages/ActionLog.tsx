import { FormEvent, useEffect, useState } from 'react';
import { apiGet, apiPost } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import { formatDate, formatDateTime } from '../lib/format';
import type { ManualAction, Recommendation } from '../types';

const emptyAction = {
  action_date: new Date().toISOString().slice(0, 10),
  action_type: 'other',
  title: '',
  description: '',
  changed_location: '',
  before_text: '',
  after_text: '',
  expected_metric: '',
  followup_date: '',
  outcome_notes: '',
  recommendation: '',
};

export function ActionLog() {
  const { selectedApp } = useAppContext();
  const [actions, setActions] = useState<ManualAction[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [form, setForm] = useState(emptyAction);
  const [message, setMessage] = useState('');

  const refresh = async () => {
    if (!selectedApp) return;
    const [actionItems, recItems] = await Promise.all([
      apiGet<{ results: ManualAction[] } | ManualAction[]>(`/manual-actions/?app=${selectedApp.id}`),
      apiGet<{ results: Recommendation[] } | Recommendation[]>(`/recommendations/?app=${selectedApp.id}`),
    ]);
    setActions(Array.isArray(actionItems) ? actionItems : actionItems.results);
    setRecommendations(Array.isArray(recItems) ? recItems : recItems.results);
  };

  useEffect(() => {
    refresh().catch(() => {
      setActions([]);
      setRecommendations([]);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedApp, message]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedApp) return;
    setMessage('');
    await apiPost('/manual-actions/', {
      app: selectedApp.id,
      recommendation: form.recommendation ? Number(form.recommendation) : null,
      action_date: form.action_date,
      action_type: form.action_type,
      title: form.title,
      description: form.description,
      changed_location: form.changed_location,
      before_text: form.before_text,
      after_text: form.after_text,
      expected_metric: form.expected_metric,
      followup_date: form.followup_date || null,
      outcome_notes: form.outcome_notes,
    });
    setForm(emptyAction);
    setMessage('Manual action logged.');
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Manual action log</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Track what changed, where, and what happened next</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
          This is the bridge between recommendations and outcomes. Capture the change now, then record the observed result later.
        </p>
      </div>

      {!selectedApp && <Card title="No app selected"><p className="text-sm text-slate-600">Select an app profile first.</p></Card>}
      {message && <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700">{message}</div>}

      {selectedApp && (
        <div className="grid gap-4 xl:grid-cols-[1fr_1fr]">
          <Card title="Log a manual action">
            <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
              <select value={form.recommendation} onChange={(event) => setForm((current) => ({ ...current, recommendation: event.target.value }))} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2">
                <option value="">Related recommendation (optional)</option>
                {recommendations.map((rec) => (
                  <option key={rec.id} value={rec.id}>
                    {rec.title}
                  </option>
                ))}
              </select>
              <input type="date" value={form.action_date} onChange={(event) => setForm((current) => ({ ...current, action_date: event.target.value }))} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              <input value={form.action_type} onChange={(event) => setForm((current) => ({ ...current, action_type: event.target.value }))} placeholder="Action type" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              <input value={form.title} onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))} placeholder="Title" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <input value={form.changed_location} onChange={(event) => setForm((current) => ({ ...current, changed_location: event.target.value }))} placeholder="Where changed" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <textarea value={form.description} onChange={(event) => setForm((current) => ({ ...current, description: event.target.value }))} placeholder="Description" className="min-h-24 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <textarea value={form.before_text} onChange={(event) => setForm((current) => ({ ...current, before_text: event.target.value }))} placeholder="Before" className="min-h-24 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <textarea value={form.after_text} onChange={(event) => setForm((current) => ({ ...current, after_text: event.target.value }))} placeholder="After" className="min-h-24 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <input value={form.expected_metric} onChange={(event) => setForm((current) => ({ ...current, expected_metric: event.target.value }))} placeholder="Expected metric" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              <input type="date" value={form.followup_date} onChange={(event) => setForm((current) => ({ ...current, followup_date: event.target.value }))} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              <textarea value={form.outcome_notes} onChange={(event) => setForm((current) => ({ ...current, outcome_notes: event.target.value }))} placeholder="Observed result later" className="min-h-24 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <button type="submit" className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white md:col-span-2">Log action</button>
            </form>
          </Card>

          <Card title="Recent actions">
            <div className="space-y-3">
              {actions.map((action) => (
                <article key={action.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-[0.22em] text-slate-500">{formatDate(action.action_date)} · {action.action_type}</p>
                  <p className="mt-2 font-semibold text-slate-900">{action.title}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{action.description}</p>
                  <p className="mt-2 text-xs text-slate-500">Where: {action.changed_location || 'n/a'}</p>
                  <p className="mt-1 text-xs text-slate-500">Observed: {action.outcome_notes || 'pending'}</p>
                  <p className="mt-1 text-xs text-slate-500">Follow up: {formatDate(action.followup_date)}</p>
                </article>
              ))}
              {actions.length === 0 && <p className="text-sm text-slate-600">No actions logged yet.</p>}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
