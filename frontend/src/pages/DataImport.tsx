import { FormEvent, useEffect, useState } from 'react';
import { apiUpload, getList } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import { formatDateTime } from '../lib/format';
import type { ImportBatch } from '../types';

type UploadKind = 'daily' | 'reviews';

export function DataImport() {
  const { selectedApp } = useAppContext();
  const [dailyFile, setDailyFile] = useState<File | null>(null);
  const [reviewFile, setReviewFile] = useState<File | null>(null);
  const [batches, setBatches] = useState<ImportBatch[]>([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!selectedApp) return;
    getList<ImportBatch>(`/import-batches/?app=${selectedApp.id}`).then(setBatches).catch(() => setBatches([]));
  }, [selectedApp, message]);

  const submit = async (kind: UploadKind, event: FormEvent) => {
    event.preventDefault();
    if (!selectedApp) return;
    const file = kind === 'daily' ? dailyFile : reviewFile;
    if (!file) {
      setMessage('Choose a CSV file first.');
      return;
    }

    const formData = new FormData();
    formData.append('app', String(selectedApp.id));
    formData.append('file', file);

    setMessage('');
    try {
      await apiUpload(kind === 'daily' ? '/imports/daily-metrics/' : '/imports/reviews/', formData);
      setMessage(`${kind === 'daily' ? 'Daily metrics' : 'Reviews'} imported successfully.`);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : 'Import failed');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Data import</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Bring in CSV exports or local extracts</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
          Imports stay local. The copilot reads the files, stores the records, and builds reports from that data.
        </p>
      </div>

      {!selectedApp && <Card title="No app selected"><p className="text-sm text-slate-600">Select an app profile first.</p></Card>}

      {selectedApp && (
        <div className="grid gap-4 xl:grid-cols-2">
          <Card title="Import daily metrics">
            <form className="space-y-4" onSubmit={(event) => submit('daily', event)}>
              <input type="file" accept=".csv,text/csv" onChange={(event) => setDailyFile(event.target.files?.[0] ?? null)} />
              <p className="text-sm text-slate-600">Expected columns include `date`, `installs`, `store_visitors`, `listing_conversion_rate`, `day_1_retention`, `day_7_retention`, and optional notes fields.</p>
              <button type="submit" className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white">Upload metrics CSV</button>
            </form>
          </Card>

          <Card title="Import reviews">
            <form className="space-y-4" onSubmit={(event) => submit('reviews', event)}>
              <input type="file" accept=".csv,text/csv" onChange={(event) => setReviewFile(event.target.files?.[0] ?? null)} />
              <p className="text-sm text-slate-600">Expected columns include `date`, `rating`, `reviewer_name`, and `review_text`.</p>
              <button type="submit" className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white">Upload reviews CSV</button>
            </form>
          </Card>
        </div>
      )}

      {message && <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700">{message}</div>}

      <Card title="Recent imports">
        <div className="space-y-3">
          {batches.length === 0 && <p className="text-sm text-slate-600">No import batches yet.</p>}
          {batches.map((batch) => (
            <article key={batch.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <p className="font-semibold text-slate-900">{batch.import_type}</p>
                <span className="text-xs uppercase tracking-[0.24em] text-slate-500">{batch.status}</span>
              </div>
              <p className="mt-2 text-sm text-slate-600">Rows: {batch.row_count}</p>
              <p className="mt-1 text-xs text-slate-500">{formatDateTime(batch.created_at)}</p>
              {batch.error_summary && <p className="mt-2 text-sm text-rose-700">{batch.error_summary}</p>}
            </article>
          ))}
        </div>
      </Card>
    </div>
  );
}
