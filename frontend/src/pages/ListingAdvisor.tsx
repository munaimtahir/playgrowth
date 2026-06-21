import { useState } from 'react';
import { apiPost } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import type { ListingAdvisorResult } from '../types';

export function ListingAdvisor() {
  const { selectedApp } = useAppContext();
  const [result, setResult] = useState<ListingAdvisorResult | null>(null);
  const [message, setMessage] = useState('');

  const generate = async () => {
    if (!selectedApp) return;
    setMessage('');
    try {
      const data = await apiPost<ListingAdvisorResult>('/listing-advisor/generate/', { app: selectedApp.id });
      setResult(data);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Unable to generate listing suggestions');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Listing advisor</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Draft honest store copy and screenshot guidance</h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
            Use these drafts as a starting point, then implement changes manually in Play Console after reviewing the trade-offs.
          </p>
        </div>
        <button type="button" onClick={generate} disabled={!selectedApp} className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white disabled:opacity-60">
          Generate drafts
        </button>
      </div>

      {!selectedApp && <Card title="No app selected"><p className="text-sm text-slate-600">Select an app profile to generate drafts.</p></Card>}
      {message && <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700">{message}</div>}

      {result && selectedApp && (
        <div className="grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
          <Card title="Current listing context">
            <p className="text-sm leading-6 text-slate-600">{result.summary}</p>
            <div className="mt-4 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-semibold text-slate-900">App</p>
              <p className="mt-1">{result.app.name}</p>
              <p className="mt-1">Package: {result.app.package_name}</p>
            </div>
          </Card>

          <Card title="Draft suggestions">
            <div className="space-y-3">
              {result.next_actions.map((rec, index) => (
                <article key={`${rec.title}-${index}`} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="font-semibold text-slate-900">{rec.title}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{rec.suggested_human_action}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{rec.copyable_text}</p>
                  <p className="mt-2 text-xs text-slate-500">Watch: {rec.watch_metric}</p>
                </article>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
