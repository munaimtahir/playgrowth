import { FormEvent, useEffect, useState } from 'react';
import { apiPatch, apiPost } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import type { AppProfile } from '../types';

const emptyForm: Omit<AppProfile, 'id'> = {
  name: '',
  package_name: '',
  play_store_url: '',
  category: 'Arcade',
  app_type: 'Game',
  primary_positioning: '',
  target_countries: '',
  monetization_model: '',
  current_version: '',
  notes: '',
};

export function AppProfile() {
  const { apps, selectedApp, selectedAppId, setSelectedAppId, refreshApps } = useAppContext();
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (selectedApp) {
      setForm({
        name: selectedApp.name || '',
        package_name: selectedApp.package_name || '',
        play_store_url: selectedApp.play_store_url || '',
        category: selectedApp.category || 'Arcade',
        app_type: selectedApp.app_type || 'Game',
        primary_positioning: selectedApp.primary_positioning || '',
        target_countries: selectedApp.target_countries || '',
        monetization_model: selectedApp.monetization_model || '',
        current_version: selectedApp.current_version || '',
        notes: selectedApp.notes || '',
      });
    }
  }, [selectedApp]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setMessage('');
    try {
      if (selectedAppId) {
        const updated = await apiPatch<AppProfile>(`/apps/${selectedAppId}/`, form);
        setMessage(`Updated ${updated.name}`);
      } else {
        const created = await apiPost<AppProfile>('/apps/', form);
        setSelectedAppId(created.id);
        setMessage(`Created ${created.name}`);
      }
      await refreshApps();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Unable to save app profile');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">App profile</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Describe the app you are trying to grow</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
          Keep the profile honest. This is the source for recommendations, report context, and the copy drafts shown elsewhere in the app.
        </p>
      </div>

      <div className="grid gap-4 xl:grid-cols-[1.3fr_0.7fr]">
        <Card title="Profile form">
          <form className="grid gap-4 md:grid-cols-2" onSubmit={submit}>
            {[
              ['name', 'App name'],
              ['package_name', 'Package name'],
              ['play_store_url', 'Play Store URL'],
              ['category', 'Category'],
              ['app_type', 'App type'],
              ['current_version', 'Current version'],
            ].map(([key, label]) => (
              <label key={key} className="block">
                <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-slate-500">{label}</span>
                <input
                  value={(form as Record<string, string>)[key]}
                  onChange={(event) => setForm((current) => ({ ...current, [key]: event.target.value }))}
                  className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-slate-400 focus:bg-white"
                />
              </label>
            ))}

            <label className="md:col-span-2">
              <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-slate-500">Primary positioning</span>
              <textarea
                value={form.primary_positioning}
                onChange={(event) => setForm((current) => ({ ...current, primary_positioning: event.target.value }))}
                className="min-h-28 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-slate-400 focus:bg-white"
              />
            </label>

            <label className="md:col-span-2">
              <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-slate-500">Target countries</span>
              <input
                value={form.target_countries}
                onChange={(event) => setForm((current) => ({ ...current, target_countries: event.target.value }))}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-slate-400 focus:bg-white"
              />
            </label>

            <label className="md:col-span-2">
              <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-slate-500">Monetization model</span>
              <input
                value={form.monetization_model}
                onChange={(event) => setForm((current) => ({ ...current, monetization_model: event.target.value }))}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-slate-400 focus:bg-white"
              />
            </label>

            <label className="md:col-span-2">
              <span className="mb-2 block text-xs uppercase tracking-[0.22em] text-slate-500">Notes</span>
              <textarea
                value={form.notes}
                onChange={(event) => setForm((current) => ({ ...current, notes: event.target.value }))}
                className="min-h-32 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-slate-400 focus:bg-white"
              />
            </label>

            <div className="md:col-span-2 flex items-center justify-between gap-4">
              <p className="text-sm text-slate-500">{message || 'Select an app or create a new profile.'}</p>
              <button type="submit" disabled={saving} className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-60">
                {saving ? 'Saving...' : selectedAppId ? 'Update profile' : 'Create profile'}
              </button>
            </div>
          </form>
        </Card>

        <Card title="Known apps">
          <div className="space-y-3">
            {apps.length === 0 && <p className="text-sm text-slate-600">No app profiles yet.</p>}
            {apps.map((app) => (
              <button
                key={app.id}
                type="button"
                onClick={() => setSelectedAppId(app.id)}
                className={`w-full rounded-2xl border px-4 py-3 text-left transition ${
                  selectedAppId === app.id ? 'border-slate-900 bg-slate-950 text-white' : 'border-slate-200 bg-slate-50 hover:border-slate-300 hover:bg-white'
                }`}
              >
                <p className="font-semibold">{app.name}</p>
                <p className={`mt-1 text-xs ${selectedAppId === app.id ? 'text-slate-300' : 'text-slate-500'}`}>{app.package_name}</p>
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
