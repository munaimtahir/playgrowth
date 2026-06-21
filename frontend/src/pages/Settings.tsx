import { Card } from '../components/Card';
import { API_BASE } from '../api/client';

const rules = [
  'No fake reviews or fake installs.',
  'No keyword stuffing or misleading claims.',
  'No Play Console writes from the software.',
  'No Google Ads budget or campaign automation in MVP.',
  'Every recommendation is a manual suggestion, not an execution command.',
];

export function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Settings</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Safety model and deployment notes</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
          These settings are mostly informational for MVP. The important behavior is that the app only recommends and logs human actions.
        </p>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <Card title="Safety rules">
          <ul className="space-y-3 text-sm leading-6 text-slate-700">
            {rules.map((rule) => (
              <li key={rule} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                {rule}
              </li>
            ))}
          </ul>
        </Card>

        <Card title="Environment">
          <div className="space-y-4 text-sm leading-6 text-slate-700">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <p className="text-xs uppercase tracking-[0.22em] text-slate-500">API base URL</p>
              <p className="mt-2 font-medium text-slate-900">{API_BASE}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <p className="text-xs uppercase tracking-[0.22em] text-slate-500">AI provider</p>
              <p className="mt-2 font-medium text-slate-900">Mock by default, no API key required</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <p className="text-xs uppercase tracking-[0.22em] text-slate-500">Data policy</p>
              <p className="mt-2 font-medium text-slate-900">Local CSV imports, manual logs, and deterministic diagnostics</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
