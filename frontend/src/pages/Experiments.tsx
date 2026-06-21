import { FormEvent, useEffect, useState } from 'react';
import { apiGet, apiPost } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import type { Experiment } from '../types';

const emptyExperiment = {
  name: '',
  hypothesis: '',
  area: 'experiment',
  variant_a: '',
  variant_b: '',
  primary_metric: '',
  secondary_metric: '',
  minimum_duration_days: 7,
  minimum_sample_size: 100,
  status: 'idea',
  result: '',
  decision: '',
};

export function Experiments() {
  const { selectedApp } = useAppContext();
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [form, setForm] = useState(emptyExperiment);
  const [message, setMessage] = useState('');

  const refresh = async () => {
    if (!selectedApp) return;
    const items = await apiGet<{ results: Experiment[] } | Experiment[]>(`/experiments/?app=${selectedApp.id}`);
    setExperiments(Array.isArray(items) ? items : items.results);
  };

  useEffect(() => {
    refresh().catch(() => setExperiments([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedApp, message]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    if (!selectedApp) return;
    setMessage('');
    await apiPost('/experiments/', { app: selectedApp.id, ...form });
    setForm(emptyExperiment);
    setMessage('Experiment saved.');
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Experiments</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Plan manual tests before making changes public</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
          Experiments document the hypothesis, the manual change, and the success rule. They are a record, not an automation loop.
        </p>
      </div>

      {!selectedApp && <Card title="No app selected"><p className="text-sm text-slate-600">Select an app profile first.</p></Card>}
      {message && <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700">{message}</div>}

      {selectedApp && (
        <div className="grid gap-4 xl:grid-cols-[1fr_1fr]">
          <Card title="Create experiment">
            <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
              <input value={form.name} onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))} placeholder="Experiment name" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <textarea value={form.hypothesis} onChange={(event) => setForm((current) => ({ ...current, hypothesis: event.target.value }))} placeholder="Hypothesis" className="min-h-28 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <input value={form.area} onChange={(event) => setForm((current) => ({ ...current, area: event.target.value }))} placeholder="Area" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              <input value={form.primary_metric} onChange={(event) => setForm((current) => ({ ...current, primary_metric: event.target.value }))} placeholder="Primary metric" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm" />
              <input value={form.variant_a} onChange={(event) => setForm((current) => ({ ...current, variant_a: event.target.value }))} placeholder="Variant A" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <input value={form.variant_b} onChange={(event) => setForm((current) => ({ ...current, variant_b: event.target.value }))} placeholder="Variant B" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm md:col-span-2" />
              <button type="submit" className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white md:col-span-2">Save experiment</button>
            </form>
          </Card>

          <Card title="Experiment backlog">
            <div className="space-y-3">
              {experiments.map((experiment) => (
                <article key={experiment.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="font-semibold text-slate-900">{experiment.name}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{experiment.hypothesis}</p>
                  <p className="mt-2 text-xs uppercase tracking-[0.22em] text-slate-500">{experiment.status}</p>
                </article>
              ))}
              {experiments.length === 0 && <p className="text-sm text-slate-600">No experiments yet.</p>}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
